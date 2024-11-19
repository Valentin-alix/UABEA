import os

from D3Database.consts import DOFUS_PATH

UABEA_PATH_EXE = os.path.join(
    "D:\\",
    "Workspace",
    "UABEA",
    "UABEAvalonia",
    "bin",
    "Debug",
    "net6.0",
    "UABEAvalonia.exe",
)


ASSEMBLIES_PATH = os.path.join(DOFUS_PATH, "assemblies")
GAME_ASSEMBLY_PATH = os.path.join(DOFUS_PATH, "GameAssembly.dll")
GLOBAL_METADATA_PATH = os.path.join(
    DOFUS_PATH, "Dofus_Data", "il2cpp_data", "Metadata", "global-metadata.dat"
)
IL2_CPP_DUMPER_PATH_EXE = os.path.join(
    os.environ["USERPROFILE"],
    "Documents",
    "Apps",
    "Il2CppDumper",
    "IL2CppDumper.exe",
)

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
