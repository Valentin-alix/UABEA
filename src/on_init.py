import os
import sys
from pathlib import Path

from src.generator.generate_python_from_datas import gen_all_python_class_datas
from src.on_maj import on_maj

sys.path.append(str(Path(__file__).parent.parent))

from db_dofus_unity.consts import (
    DOFUS_PATH,
)

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


def get_gfx():
    os.system(
        f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets","Content", "Picto", "Items")}"
    )


def get_datas():
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
    # get_gfx()
    on_maj()
    get_datas()
    gen_all_python_class_datas()
