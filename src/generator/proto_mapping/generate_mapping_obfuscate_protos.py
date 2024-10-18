import json
import os
import sys
from pathlib import Path
from typing import Iterator

import icecream

from src.generator.proto_mapping.comparator.proto_comparator import (
    ProtoComparator,
    ProtoInfo,
)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


from src.consts import (
    OBFUSCATED_PROTO_GAME,
    PROTO_GAME_PATH,
    PROTO_CONNECTION_PATH,
    OBFUSCATED_PROTO_CONNECTION,
    MAPPING_CONN_PROTO_PATH,
    MAPPING_GAME_PROTO_PATH,
)
from proto_schema_parser.parser import Parser
from proto_schema_parser.ast import Message, FileElement, Enum


def iter_element_from_dir(input_folder: str) -> Iterator[FileElement]:
    for root, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            if not filename.endswith(".proto"):
                continue
            with open(os.path.join(root, filename)) as file:
                datas = file.read()
                res = Parser().parse(datas)
                for element in res.file_elements:
                    yield element


def get_mapping_protos(old_proto_path: str, obfuscated_proto_path: str):
    old_message_by_name: dict[str, Message] = {}
    old_enum_by_name: dict[str, Enum] = {}
    for new_elem in iter_element_from_dir(old_proto_path):
        if type(new_elem) is Message:
            old_message_by_name[new_elem.name] = new_elem
        elif type(new_elem) is Enum:
            old_enum_by_name[new_elem.name] = new_elem

    new_message_by_name: dict[str, Message] = {}
    new_enum_by_name: dict[str, Enum] = {}
    for new_elem in iter_element_from_dir(obfuscated_proto_path):
        if type(new_elem) is Message:
            new_message_by_name[new_elem.name] = new_elem
        elif type(new_elem) is Enum:
            new_enum_by_name[new_elem.name] = new_elem

    mapping = ProtoComparator(
        old_proto_info=ProtoInfo(
            message_by_name=old_message_by_name, enum_by_name=old_enum_by_name
        ),
        new_proto_info=ProtoInfo(
            message_by_name=new_message_by_name, enum_by_name=new_enum_by_name
        ),
    ).get_most_probable_message_mapping()

    icecream.ic(mapping)
    # icecream.ic(sorted(mapping.items(), key=lambda elem: elem[1][1]))

    # message_names = [msg[1][0] for msg in mapping.items()]
    # name_counts = Counter(message_names)
    # duplicate_names = [
    #     (name, count) for name, count in name_counts.items() if count > 1
    # ]
    #
    # print(duplicate_names)

    return mapping


if __name__ == "__main__":
    conn_mapping = get_mapping_protos(
        PROTO_CONNECTION_PATH, OBFUSCATED_PROTO_CONNECTION
    )
    with open(MAPPING_CONN_PROTO_PATH, "w+") as file:
        json.dump(conn_mapping, file)

    game_mapping = get_mapping_protos(PROTO_GAME_PATH, OBFUSCATED_PROTO_GAME)
    with open(MAPPING_GAME_PROTO_PATH, "w+") as file:
        json.dump(game_mapping, file)
