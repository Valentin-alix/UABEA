import os
from pathlib import Path

DOFUS_PATH = os.path.join(
    os.environ["USERPROFILE"], "AppData", "Local", "Ankama", "Dofus-beta"
)

OBFUSCATED_PROTOS = os.path.join(DOFUS_PATH, "protocol")
OBFUSCATED_PROTO_CONNECTION = os.path.join(OBFUSCATED_PROTOS, "connection")
OBFUSCATED_PROTO_GAME = os.path.join(OBFUSCATED_PROTOS, "game")


DOFUS_ASSETS_FOLDER = os.path.join(DOFUS_PATH, "Dofus_Data", "StreamingAssets")
DOFUS_CONTENT_FOLDER = os.path.join(DOFUS_ASSETS_FOLDER, "Content")

DOFUS_DATA_PATH = os.path.join(DOFUS_CONTENT_FOLDER, "Data", "exported")
DOFUS_MAP_PATH = os.path.join(DOFUS_CONTENT_FOLDER, "Map", "exported")
DOFUS_STANDALONE_PATH = os.path.join(
    DOFUS_ASSETS_FOLDER, "aa", "StandaloneWindows64", "exported"
)
I18N_PATH = os.path.join(DOFUS_CONTENT_FOLDER, "I18n", "fr.bin")
WORLD_GRAPH_FILENAME = "worldgraph.json"

OUTPUT_PATH = os.path.join(Path(__file__).parent.parent, "outputs")

PROTO_ROOT_PATH = os.path.join(OUTPUT_PATH, "protos")
PROTO_CONNECTION_PATH = os.path.join(PROTO_ROOT_PATH, "connection")
PROTO_GAME_PATH = os.path.join(PROTO_ROOT_PATH, "game")

OUTPUT_CLASS_GEN = os.path.join(OUTPUT_PATH, "gen")
OUTPUT_CLASS_DATAS = os.path.join(OUTPUT_CLASS_GEN, "gen_datas")
OUTPUT_CLASS_MAPS = os.path.join(OUTPUT_CLASS_GEN, "gen_maps")
OUTPUT_CLASS_STANDALONE = os.path.join(OUTPUT_CLASS_GEN, "gen_standalone")
