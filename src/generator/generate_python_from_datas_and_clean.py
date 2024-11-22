import json
import os
from collections import defaultdict
from pathlib import Path
from tempfile import NamedTemporaryFile

import msgspec.json
from D3Database.consts import (
    WORLD_GRAPH_FILENAME,
    D3_MAP,
)
from D3Database.models.maps import MapData
from D3Database.models.world_graph import WorldGraphData
from msgspec import Struct
from tqdm import tqdm

from src.utils import instantiate_class_from_path


def run_cmd_codegen(
    input_filename: str, output_filename: str, base_folder: str | None = None
) -> None:
    cmd = (
        f"datamodel-codegen --input-file-type json --input {input_filename} --output {output_filename} --custom"
        f"-template-dir {os.path.join(Path(__file__).parent, "template")}  --output-model-type msgspec.Struct "
        f"--encoding utf-8 --target-python-version 3.12 --keyword-only"
    )
    extra_data: dict[str, dict] = defaultdict(dict)
    if base_folder is not None:
        filepath = os.path.relpath(input_filename, base_folder)
        extra_data["Model"]["filepath"] = filepath

    with NamedTemporaryFile(mode="r+", suffix=".json", delete=False) as file:
        json.dump(extra_data, file)

    cmd += f" --extra-template-data {file.name}"
    os.system(cmd)


def gen_and_clean_datas(base_folder: str, input_folder: str, output_folder: str):
    for filename in os.listdir(input_folder):
        if not filename.endswith(".json"):
            continue
        print(f"processing data {filename}")
        file_path = os.path.join(input_folder, filename)
        python_filename = filename.split(".json")[0] + ".py"
        run_cmd_codegen(
            file_path, os.path.join(output_folder, python_filename), base_folder
        )
        if os.path.exists(os.path.join(output_folder, python_filename)):
            class_type = instantiate_class_from_path(
                "Model",
                os.path.join(output_folder, python_filename),
            )
            with open(file_path, "rb") as file:
                content = msgspec.json.decode(file.read(), type=class_type)
            with open(file_path, "wb") as file:
                file.write(msgspec.json.encode(content))


def clean_map_datas(input_folder: str):
    print("cleaning map folder..")
    for filename in tqdm(os.listdir(input_folder)):
        if not filename.startswith("map_") or not filename.endswith(".json"):
            continue
        file_path = os.path.join(input_folder, filename)
        with open(file_path, "rb") as file:
            content = msgspec.json.decode(file.read(), type=MapData)
        with open(file_path, "wb") as file:
            file.write(msgspec.json.encode(content))


def gen_and_clean_world_graph_datas(input_folder: str):
    file_path = os.path.join(input_folder, WORLD_GRAPH_FILENAME)
    print("cleaning world graph")
    with open(file_path, "rb") as file:
        content: Struct = msgspec.json.decode(file.read(), type=WorldGraphData)
    with open(file_path, "wb") as file:
        file.write(msgspec.json.encode(content))


def gen_and_clean_python_class_datas():
    # gen_and_clean_datas(D3_DATABASE, D3_DATA, OUTPUT_CLASS_DATAS)
    # gen_and_clean_world_graph_datas(D3_STANDALONE)
    clean_map_datas(D3_MAP)


if __name__ == "__main__":
    gen_and_clean_python_class_datas()
