import os
import sys
from pathlib import Path

from tqdm import tqdm

from src.generator.generate_python_from_datas_and_clean import (
    gen_and_clean_python_class_datas,
)
from src.on_maj import on_maj

sys.path.append(str(Path(__file__).parent.parent))

from src.consts import UABEA_PATH_EXE
from D3Database.consts import (
    DOFUS_PATH,
    D3_STANDALONE,
    D3_MAP,
    D3_DATA,
)

PATH_STANDALONE_BUNDLES = os.path.join(
    DOFUS_PATH, "Dofus_Data", "StreamingAssets", "aa", "StandaloneWindows64"
)
PATH_MAPS = os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets", "Content", "Map")


def get_world_graph_datas():
    for filename in os.listdir(PATH_STANDALONE_BUNDLES):
        if "worldassets_assets_all" not in filename:
            continue
        os.system(
            f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(PATH_STANDALONE_BUNDLES, filename)} -out {D3_STANDALONE}"
        )

    for filename in os.listdir(D3_STANDALONE):
        if filename == "worldgraph.json":
            continue
        os.remove(os.path.join(D3_STANDALONE, filename))


def get_map_datas():
    for filename in tqdm(os.listdir(PATH_MAPS)):
        if "mapdata_assets_world" not in filename or not filename.endswith(".bundle"):
            continue
        os.system(
            f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(PATH_MAPS, filename)} -out {D3_MAP}"
        )


def get_datas():
    os.system(
        f"{UABEA_PATH_EXE} batchexportbundle {os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets", "Content", "Data")} -out {D3_DATA}"
    )


if __name__ == "__main__":
    on_maj()
    get_map_datas()
    get_world_graph_datas()
    get_datas()
    gen_and_clean_python_class_datas()
