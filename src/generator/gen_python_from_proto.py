import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from D3Database.consts import PROTO_CONNECTION_PATH, PROTO_GAME_PATH


def gen_python_from_protoc(input_folder: str, output_folder: str):
    for filename in os.listdir(input_folder):
        if not filename.endswith(".proto"):
            continue
        file_path = os.path.join(input_folder, filename)
        os.system(
            f"protoc --proto_path={input_folder} --python_out={output_folder} {file_path} --pyi_out={output_folder}"
        )


def gen_all_python_from_protoc():
    gen_python_from_protoc(PROTO_CONNECTION_PATH, PROTO_CONNECTION_PATH)
    gen_python_from_protoc(PROTO_GAME_PATH, PROTO_GAME_PATH)


if __name__ == "__main__":
    gen_all_python_from_protoc()
