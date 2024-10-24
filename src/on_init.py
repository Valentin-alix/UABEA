import os
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from db_dofus_unity.consts import (
    DOFUS_PATH,
)
from src.on_maj import on_maj
from src.generator.generate_python_from_datas import gen_all_python_class_datas


def get_datas():
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
    on_maj()
    get_datas()
    gen_all_python_class_datas()
