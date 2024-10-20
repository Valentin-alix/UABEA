import json
import os

from icecream import icecream
from proto_schema_parser.ast import Message, Enum, File, Package, Import
from proto_schema_parser.parser import Parser

from db_dofus_unity.consts import (
    PROTO_GAME_PATH,
    PROTO_CONNECTION_PATH,
    MAPPING_CONN_PROTO_PATH,
    MAPPING_GAME_PROTO_PATH,
    OBFUSCATED_PROTO_CONNECTION,
    OBFUSCATED_PROTO_GAME,
)
from db_dofus_unity.generator.comparator.models.proto_file_info import ProtoFileInfo
from db_dofus_unity.generator.comparator.proto_comparator import (
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
    proto_file_info = ProtoFileInfo(filename=filename)

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
    mapping = ProtoComparator(
        old_proto_files_infos=get_proto_info_by_filename(old_proto_path),
        new_proto_files_infos=get_proto_info_by_filename(obfuscated_proto_path),
    ).get_messages_mapping()

    icecream.ic(sorted(mapping.items(), key=lambda elem: elem[1].similarity)[:10])

    return mapping


def get_most_probable_mapping_protos(old_proto_path: str, obfuscated_proto_path: str):
    mapping = ProtoComparator(
        old_proto_files_infos=get_proto_info_by_filename(old_proto_path),
        new_proto_files_infos=get_proto_info_by_filename(obfuscated_proto_path),
    ).get_most_probable_messages_mapping()

    icecream.ic(mapping)

    return mapping


def main():
    conn_mapping = get_most_probable_mapping_protos(
        PROTO_CONNECTION_PATH, OBFUSCATED_PROTO_CONNECTION
    )
    with open(MAPPING_CONN_PROTO_PATH, "w+") as file:
        json.dump(conn_mapping, file)

    game_mapping = get_most_probable_mapping_protos(
        PROTO_GAME_PATH, OBFUSCATED_PROTO_GAME
    )
    with open(MAPPING_GAME_PROTO_PATH, "w+") as file:
        json.dump(game_mapping, file)


def main_debug():
    get_mapping_protos(PROTO_CONNECTION_PATH, OBFUSCATED_PROTO_CONNECTION)
    get_mapping_protos(PROTO_GAME_PATH, OBFUSCATED_PROTO_GAME)


if __name__ == "__main__":
    main()
