import os
import sys
from pathlib import Path
from typing import Iterator

import icecream

from src.generator.comparator.proto_comparator import (
    ProtoComparator,
    ProtoInfo,
)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


from src.consts import (
    OBFUSCATED_PROTO_GAME,
    PROTO_GAME_PATH,
    PROTO_CONNECTION_PATH,
    OBFUSCATED_PROTO_CONNECTION,
)
from proto_schema_parser.parser import Parser
from proto_schema_parser.ast import Message, Enum, File, Package


def iter_proto_file_from_dir(input_folder: str) -> Iterator[File]:
    for root, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            if not filename.endswith(".proto"):
                continue
            with open(os.path.join(root, filename)) as file:
                datas = file.read()
                res = Parser().parse(datas)
                yield res


def get_complete_name(path: str | None, name: str) -> str:
    if path is None:
        return name
    return f"{path}.{name}"


def get_proto_info_from_elem(path: str | None, elem: Message | Enum):
    message_by_import_name: dict[str, Message] = {}
    enum_by_import_name: dict[str, Enum] = {}

    if type(elem) is Message:
        message_by_import_name[get_complete_name(path, elem.name)] = elem
        for sub_elem in elem.elements:
            if not (type(sub_elem) is Message or type(sub_elem) is Enum):
                continue
            sub_path: str | None = f"{path}.{elem.name}" if path is not None else None
            sub_message_by_import_name, sub_enum_by_import_name = (
                get_proto_info_from_elem(sub_path, sub_elem)
            )
            message_by_import_name |= sub_message_by_import_name
            enum_by_import_name |= sub_enum_by_import_name

    elif type(elem) is Enum:
        enum_by_import_name[get_complete_name(path, elem.name)] = elem

    return message_by_import_name, enum_by_import_name


def get_proto_info(proto_path: str) -> ProtoInfo:
    root_messages: list[Message] = []
    message_by_import_name: dict[str, Message] = {}
    enum_by_import_name: dict[str, Enum] = {}
    for proto_file in iter_proto_file_from_dir(proto_path):
        package: str | None = None
        for file_elem in proto_file.file_elements:
            if type(file_elem) is Package:
                package = file_elem.name

            if type(file_elem) is Message:
                root_messages.append(file_elem)

            if type(file_elem) is Message or type(file_elem) is Enum:
                sub_message_by_import_name, sub_enum_by_import_name = (
                    get_proto_info_from_elem(package, file_elem)
                )
                message_by_import_name |= sub_message_by_import_name
                enum_by_import_name |= sub_enum_by_import_name

    return ProtoInfo(
        root_messages=root_messages,
        enum_by_import_name=enum_by_import_name,
        message_by_import_name=message_by_import_name,
    )


def get_mapping_protos(old_proto_path: str, obfuscated_proto_path: str):
    mapping = ProtoComparator(
        old_proto_info=get_proto_info(old_proto_path),
        new_proto_info=get_proto_info(obfuscated_proto_path),
    ).get_messages_mapping()

    icecream.ic(mapping)
    # icecream.ic(sorted(mapping.items(), key=lambda elem: elem[1][1]))

    return mapping


if __name__ == "__main__":
    conn_mapping = get_mapping_protos(
        PROTO_CONNECTION_PATH, OBFUSCATED_PROTO_CONNECTION
    )
    # with open(MAPPING_CONN_PROTO_PATH, "w+") as file:
    #     json.dump(conn_mapping, file)

    game_mapping = get_mapping_protos(PROTO_GAME_PATH, OBFUSCATED_PROTO_GAME)
    # with open(MAPPING_GAME_PROTO_PATH, "w+") as file:
    #     json.dump(game_mapping, file)
