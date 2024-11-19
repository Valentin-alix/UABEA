import os
import sys
from pathlib import Path

from src.generator.generate_python_from_datas_and_clean import (
    gen_and_clean_python_class_datas,
)
from src.on_maj import on_maj

sys.path.append(str(Path(__file__).parent.parent))

from src.consts import UABEA_PATH_EXE
from D3Database.consts import (
    D3_STANDALONE,
    DOFUS_PATH,
    D3_DATA,
    D3_MAP,
    D3_GFX,
)


def get_gfx():
    os.system(
        f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets", "Content", "Characters", "Skins")} -out {D3_GFX}"
    )


def get_datas():
    os.system(
        f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets", "Content", "Map")} -out {D3_MAP}"
    )
    for filename in os.listdir(D3_MAP):
        if not filename.startswith("map_"):
            os.remove(os.path.join(D3_MAP, filename))

    os.system(
        f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets", "aa", "StandaloneWindows64")} -out {D3_STANDALONE}"
    )
    for filename in os.listdir(D3_STANDALONE):
        if filename != "worldgraph.json":
            os.remove(os.path.join(D3_STANDALONE, filename))

    os.system(
        f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets", "Content", "Data")} -out {D3_DATA}"
    )


if __name__ == "__main__":
    on_maj()
    get_datas()
    gen_and_clean_python_class_datas()
