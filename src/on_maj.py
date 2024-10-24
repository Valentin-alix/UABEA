import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from db_dofus_unity.consts import (
    DOFUS_PATH,
    OBFUSCATED_PROTO_CONNECTION,
    OBFUSCATED_PROTO_GAME,
)
from src.generator.generate_mapping_obfuscate_protos import generate_mapping_proto
from src.generator.generate_python_from_proto import gen_all_python_from_protoc

ASSEMBLIES_PATH = os.path.join(DOFUS_PATH, "assemblies")


def get_assemblies():
    os.makedirs(ASSEMBLIES_PATH, exist_ok=True)
    GAME_ASSEMBLY_PATH = os.path.join(DOFUS_PATH, "GameAssembly.dll")
    GLOBAL_METADATA_PATH = os.path.join(
        DOFUS_PATH, "Dofus_Data", "il2cpp_data", "Metadata", "global-metadata.dat"
    )
    IL2CPPDUMPER_PATH_EXE = os.path.join(
        os.environ["USERPROFILE"],
        "Documents",
        "Apps",
        "Il2CppDumper",
        "IL2CppDumper.exe",
    )

    command = f"{IL2CPPDUMPER_PATH_EXE} {GAME_ASSEMBLY_PATH} {GLOBAL_METADATA_PATH} {ASSEMBLIES_PATH}"
    os.system(command)


def get_protos():
    PROTO_CONNECTION_ASSEMBLY_PATH = os.path.join(
        ASSEMBLIES_PATH, "DummyDll", "Ankama.Dofus.Protocol.Connection.dll"
    )
    PROTO_GAME_ASSEMBLY_PATH = os.path.join(
        ASSEMBLIES_PATH, "DummyDll", "Ankama.Dofus.Protocol.Game.dll"
    )
    PROTODEC_PATH_EXE = os.path.join(
        "D:\\",
        "Workspace",
        "protodec",
        "bin",
        "protodec",
        "Debug",
        "net8.0",
        "protodec.exe",
    )
    os.makedirs(OBFUSCATED_PROTO_CONNECTION, exist_ok=True)
    os.makedirs(OBFUSCATED_PROTO_GAME, exist_ok=True)

    os.system(
        f"{PROTODEC_PATH_EXE} {PROTO_CONNECTION_ASSEMBLY_PATH} {OBFUSCATED_PROTO_CONNECTION}"
    )
    os.system(f"{PROTODEC_PATH_EXE} {PROTO_GAME_ASSEMBLY_PATH} {OBFUSCATED_PROTO_GAME}")


def on_maj():
    get_assemblies()
    get_protos()
    generate_mapping_proto()
    gen_all_python_from_protoc()


if __name__ == "__main__":
    on_maj()
