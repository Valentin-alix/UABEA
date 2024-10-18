import itertools
import os
from pathlib import Path
import sys
from typing import Iterator

from icecream import ic


sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from src.generator.proto_mapping.similarity.similarity_message import (
    compare_messages,
)
from src.consts import (
    OBFUSCATED_PROTO_GAME,
    PROTO_GAME_PATH,
    PROTO_CONNECTION_PATH,
    OBFUSCATED_PROTO_CONNECTION,
)
from proto_schema_parser.parser import Parser
from proto_schema_parser.ast import Message


def iter_element_from_dir(input_folder: str) -> Iterator[Message]:
    for root, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            if not filename.endswith(".proto"):
                continue
            with open(os.path.join(root, filename)) as file:
                datas = file.read()
                res = Parser().parse(datas)
                for element in res.file_elements:
                    if not isinstance(element, Message):
                        continue
                    yield element


def get_mapping_protos(old_proto_path: str, obfuscated_proto_path: str):
    mapping: dict[str, tuple[str, float]] = {}

    old_messages: dict[str, Message] = {}
    for msg in iter_element_from_dir(old_proto_path):
        old_messages[msg.name] = msg

    for msg in iter_element_from_dir(obfuscated_proto_path):
        mapping_by_sim: dict[str, float] = {}
        for old_msg in old_messages.values():
            if msg.name == "hgh" and old_msg.name == "CharacterPresetInfo":
                print()
            similarity = compare_messages(old_msg, msg)
            if similarity == 1:
                mapping[msg.name] = (old_messages[old_msg.name].name, 1)
                break
            mapping_by_sim[old_msg.name] = compare_messages(old_msg, msg)
        else:
            probable_matching = max(
                mapping_by_sim.items(), key=lambda elem: elem[1], default=("", 0.0)
            )
            mapping[msg.name] = probable_matching

    ic(sorted(mapping.items(), key=lambda elem: elem[1][1]))


if __name__ == "__main__":
    get_mapping_protos(PROTO_CONNECTION_PATH, OBFUSCATED_PROTO_CONNECTION)
    get_mapping_protos(PROTO_GAME_PATH, OBFUSCATED_PROTO_GAME)
