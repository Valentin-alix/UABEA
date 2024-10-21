import os

from db_dofus_unity.consts import DOFUS_PATH, OBFUSCATED_PROTO_CONNECTION, OBFUSCATED_PROTO_GAME
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
        os.environ["USERPROFILE"],
        "Documents",
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


def get_datas():
    UABEA_PATH_EXE = os.path.join(
        os.environ["USERPROFILE"],
        "Documents",
        "Workspace",
        "UABEA",
        "UABEAvalonia",
        "bin",
        "Debug",
        "net6.0",
        "UABEAvalonia.exe",
    )

    os.system(
        f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets", "Content", "Map")}"
    )
    os.system(
        f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets", "aa", "StandaloneWindows64")}"
    )
    os.system(
        f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets", "Content", "Data")}"
    )


if __name__ == "__main__":
    get_assemblies()
    get_protos()
    gen_all_python_from_protoc()
    # gen_all_python_class_datas()
