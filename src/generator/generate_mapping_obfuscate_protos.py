import json

from db_dofus_unity.consts import (
    PROTO_CONNECTION_PATH,
    OBFUSCATED_PROTO_CONNECTION,
    PROTO_GAME_PATH,
    OBFUSCATED_PROTO_GAME,
    MAPPING_GAME_PROTO_PATH,
    MAPPING_CONN_PROTO_PATH,
)
from src.generator.p_comparator.factories.p_folder_factory import PFolderFactory
from src.generator.p_comparator.p_comparator import PComparator


def generate_mapping_proto():
    old_p_folder_conn = PFolderFactory.create_p_folder(PROTO_CONNECTION_PATH)
    new_p_folder_conn = PFolderFactory.create_p_folder(OBFUSCATED_PROTO_CONNECTION)
    mapping_conn = PComparator(
        new_p_folder=new_p_folder_conn, old_p_folder=old_p_folder_conn
    ).get_mapping()
    with open(MAPPING_CONN_PROTO_PATH, "w+") as file:
        json.dump(mapping_conn, file, indent=2)

    old_p_folder_game = PFolderFactory.create_p_folder(PROTO_GAME_PATH)
    new_p_folder_game = PFolderFactory.create_p_folder(OBFUSCATED_PROTO_GAME)
    mapping_game = PComparator(
        new_p_folder=new_p_folder_game, old_p_folder=old_p_folder_game
    ).get_mapping()
    with open(MAPPING_GAME_PROTO_PATH, "w+") as file:
        json.dump(mapping_game, file, indent=2)


if __name__ == "__main__":
    generate_mapping_proto()
