import os
import sys
from pathlib import Path

from src.generator.gen_mapping_proto import generate_mapping_proto
from src.generator.gen_python_from_proto import gen_all_python_from_protoc

sys.path.append(str(Path(__file__).parent.parent))

from src.consts import (
    IL2_CPP_DUMPER_PATH_EXE,
    GAME_ASSEMBLY_PATH,
    GLOBAL_METADATA_PATH,
    PROTODEC_PATH_EXE,
    PROTO_CONNECTION_ASSEMBLY_PATH,
    PROTO_GAME_ASSEMBLY_PATH,
    ASSEMBLIES_PATH,
)
from D3Database.consts import (
    OBFUSCATED_PROTO_CONNECTION,
    OBFUSCATED_PROTO_GAME,
)


def get_assemblies():
    os.makedirs(ASSEMBLIES_PATH, exist_ok=True)
    command = f"{IL2_CPP_DUMPER_PATH_EXE} {GAME_ASSEMBLY_PATH} {GLOBAL_METADATA_PATH} {ASSEMBLIES_PATH}"
    os.system(command)


def get_protos():
    os.makedirs(OBFUSCATED_PROTO_CONNECTION, exist_ok=True)
    for filename in os.listdir(OBFUSCATED_PROTO_CONNECTION):
        if filename.endswith(".proto"):
            os.remove(os.path.join(OBFUSCATED_PROTO_CONNECTION, filename))
    os.system(
        f"{PROTODEC_PATH_EXE} {PROTO_CONNECTION_ASSEMBLY_PATH} {OBFUSCATED_PROTO_CONNECTION}"
    )

    os.makedirs(OBFUSCATED_PROTO_GAME, exist_ok=True)
    for filename in os.listdir(OBFUSCATED_PROTO_GAME):
        if filename.endswith(".proto"):
            os.remove(os.path.join(OBFUSCATED_PROTO_GAME, filename))
    os.system(f"{PROTODEC_PATH_EXE} {PROTO_GAME_ASSEMBLY_PATH} {OBFUSCATED_PROTO_GAME}")


def gen_mapping_and_python_from_proto():
    get_assemblies()
    get_protos()
    generate_mapping_proto()
    gen_all_python_from_protoc()


if __name__ == "__main__":
    gen_mapping_and_python_from_proto()
