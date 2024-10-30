import json
import os

from icecream import icecream
from proto_schema_parser.ast import Message, Enum, File, Package, Import
from proto_schema_parser.parser import Parser

from db_dofus_unity.consts import (
    PROTO_GAME_PATH,
    PROTO_CONNECTION_PATH,
    MAPPING_CONN_PROTO_PATH,
    OBFUSCATED_PROTO_CONNECTION,
    OBFUSCATED_PROTO_GAME,
    MAPPING_GAME_PROTO_PATH,
)
from src.generator.comparator.models.proto_file_info import ProtoFileInfo
from src.generator.comparator.proto_comparator import (
    ProtoComparator,
)


def get_proto_info_by_filename(proto_path: str) -> dict[str, ProtoFileInfo]:
    proto_info_by_filename: dict[str, ProtoFileInfo] = {}
    for filename, proto_file in get_proto_file_by_filename_from_dir(proto_path).items():
        proto_info_by_filename[filename] = get_proto_file_info(filename, proto_file)
    return proto_info_by_filename


def get_proto_file_by_filename_from_dir(input_folder: str) -> dict[str, File]:
    proto_file_by_filename: dict[str, File] = {}
    for root, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            if not filename.endswith(".proto"):
                continue
            with open(os.path.join(root, filename)) as file:
                datas = file.read()
            proto_file_by_filename[filename] = Parser().parse(datas)
    return proto_file_by_filename


def get_proto_file_info(filename: str, proto_file: File) -> ProtoFileInfo:
    proto_file_info = ProtoFileInfo(origin_file=proto_file, filename=filename)

    for file_elem in proto_file.file_elements:
        if type(file_elem) is Import:
            proto_file_info.imports.append(file_elem)
        elif type(file_elem) is Package:
            proto_file_info.package = file_elem
        elif type(file_elem) is Message:
            proto_file_info.messages.append(file_elem)
        elif type(file_elem) is Enum:
            proto_file_info.enums.append(file_elem)

    return proto_file_info


def get_mapping_protos(old_proto_path: str, obfuscated_proto_path: str):
    mapping, _ = ProtoComparator(
        old_proto_files_infos=get_proto_info_by_filename(old_proto_path),
        new_proto_files_infos=get_proto_info_by_filename(obfuscated_proto_path),
    ).get_all_messages_mapping()

    icecream.ic(sorted(mapping.items(), key=lambda elem: elem[1].similarity)[:10])

    return mapping


def get_most_probable_mapping_protos_with_generated_file(
    old_proto_path: str, obfuscated_proto_path: str
) -> tuple[dict[str, str], dict[str, str]]:
    mapping, generated_file_by_name = ProtoComparator(
        old_proto_files_infos=get_proto_info_by_filename(old_proto_path),
        new_proto_files_infos=get_proto_info_by_filename(obfuscated_proto_path),
    ).get_all_messages_mapping()

    most_probable_mapping = {
        (
            mapping_info.messages_index_with_name[0][1]
            if len(mapping_info.messages_index_with_name) > 0
            else ""
        ): old_msg_name
        for old_msg_name, mapping_info in mapping.items()
    }

    return most_probable_mapping, generated_file_by_name


def generate_mapping_proto():
    conn_mapping, conn_generated_file_by_name = (
        get_most_probable_mapping_protos_with_generated_file(
            PROTO_CONNECTION_PATH, OBFUSCATED_PROTO_CONNECTION
        )
    )
    for name, file_content in conn_generated_file_by_name.items():
        with open(os.path.join(PROTO_CONNECTION_PATH, "generated", name), "w+") as file:
            file.write(file_content)
    with open(MAPPING_CONN_PROTO_PATH, "w+") as file:
        json.dump(conn_mapping, file, indent=2)

    game_mapping, game_generated_file_by_name = (
        get_most_probable_mapping_protos_with_generated_file(
            PROTO_GAME_PATH, OBFUSCATED_PROTO_GAME
        )
    )
    for name, file_content in game_generated_file_by_name.items():
        with open(os.path.join(PROTO_GAME_PATH, "generated", name), "w+") as file:
            file.write(file_content)
    with open(MAPPING_GAME_PROTO_PATH, "w+") as file:
        json.dump(game_mapping, file, indent=2)


def main_debug():
    get_mapping_protos(PROTO_CONNECTION_PATH, OBFUSCATED_PROTO_CONNECTION)
    get_mapping_protos(PROTO_GAME_PATH, OBFUSCATED_PROTO_GAME)


if __name__ == "__main__":
    main_debug()
