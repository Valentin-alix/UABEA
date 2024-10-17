import os
from pathlib import Path
import sys
from typing import Iterator

from icecream import ic


sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from src.generator.proto_mapping.complexity.msg_complexity import get_msg_complexity
from src.generator.proto_mapping.similarity.similarity_message import (
    compare_similarity_message,
)
from src.consts import (
    OBFUSCATED_PROTO_CONNECTION,
    OBFUSCATED_PROTO_GAME,
    PROTO_CONNECTION_PATH,
    PROTO_GAME_PATH,
)
from proto_schema_parser.parser import Parser
from proto_schema_parser.ast import Message


def iter_element_from_dir(input_folder: str) -> Iterator[Message]:
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if not file.endswith(".proto"):
                continue
            with open(os.path.join(root, file)) as file:
                datas = file.read()
                res = Parser().parse(datas)
                for element in res.file_elements:
                    if not isinstance(element, Message):
                        continue
                    yield element


def get_mapping_protos(old_proto_path: str, obfuscated_proto_path: str):
    mapping: dict[str, str] = {}

    old_messages: list[Message] = []
    for msg in iter_element_from_dir(old_proto_path):
        old_messages.append(msg)

    new_msgs = list(iter_element_from_dir(obfuscated_proto_path))
    new_msgs.sort(key=lambda elem: get_msg_complexity(elem), reverse=True)
    for msg in iter_element_from_dir(obfuscated_proto_path):
        found_msg: Message | None = None
        for old_msg in old_messages:
            if compare_similarity_message(old_msg, msg):
                found_msg = old_msg
                mapping[msg.name] = found_msg.name
                break

        if found_msg:
            old_messages.remove(found_msg)
        else:
            print(f"not found : {msg.name}")

    ic(mapping)


if __name__ == "__main__":
    get_mapping_protos(PROTO_CONNECTION_PATH, OBFUSCATED_PROTO_CONNECTION)
    get_mapping_protos(PROTO_GAME_PATH, OBFUSCATED_PROTO_GAME)
