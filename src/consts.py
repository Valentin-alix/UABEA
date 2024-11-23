import os
from pathlib import Path

from D3Database.consts import DOFUS_PATH

UABEA_PATH_EXE = os.path.join(
    Path(__file__).parent.parent,
    "UABEA",
    "UABEAvalonia",
    "bin",
    "Debug",
    "net6.0",
    "UABEAvalonia.exe",
)
IL2_CPP_DUMPER_PATH_EXE = os.path.join(
    Path(__file__).parent.parent, "Il2CppDumper", "IL2CppDumper.exe"
)


ASSEMBLIES_PATH = os.path.join(DOFUS_PATH, "assemblies")
GAME_ASSEMBLY_PATH = os.path.join(DOFUS_PATH, "GameAssembly.dll")
GLOBAL_METADATA_PATH = os.path.join(
    DOFUS_PATH, "Dofus_Data", "il2cpp_data", "Metadata", "global-metadata.dat"
)


PROTO_CONNECTION_ASSEMBLY_PATH = os.path.join(
    ASSEMBLIES_PATH, "DummyDll", "Ankama.Dofus.Protocol.Connection.dll"
)
PROTO_GAME_ASSEMBLY_PATH = os.path.join(
    ASSEMBLIES_PATH, "DummyDll", "Ankama.Dofus.Protocol.Game.dll"
)
PROTODEC_PATH_EXE = os.path.join(
    Path(__file__).parent.parent,
    "protodec",
    "bin",
    "protodec",
    "Debug",
    "net8.0",
    "protodec.exe",
)
