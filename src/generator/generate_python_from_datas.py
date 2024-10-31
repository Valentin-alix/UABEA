import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from tqdm import tqdm

from db_dofus_unity.consts import (
    WORLD_GRAPH_FILENAME,
    DOFUS_PATH,
    DOFUS_DATA_PATH,
    OUTPUT_CLASS_DATAS,
    DOFUS_MAP_PATH,
    OUTPUT_CLASS_MAPS,
    DOFUS_STANDALONE_PATH,
    OUTPUT_CLASS_STANDALONE,
)


def run_cmd_codegen(
    input_filename: str,
    output_filename: str,
    base_dofus_folder: str | None = None,
):
    cmd = f"datamodel-codegen --input-file-type json --input {input_filename} --reuse-model --output {output_filename} --custom-template-dir {os.path.join(Path(__file__).parent, "template")}  --output-model-type msgspec.Struct"
    if base_dofus_folder:
        extra_data: dict[str, dict] = {"Model": {}, "#all#": {}}
        filepath = os.path.relpath(input_filename, base_dofus_folder)
        extra_data["Model"]["filepath"] = filepath
        with NamedTemporaryFile(mode="r+", suffix=".json", delete=False) as file:
            json.dump(extra_data, file)
        cmd += f" --extra-template-data {file.name}"
    os.system(cmd)


def gen_datas(base_dofus_folder: str, input_folder: str, output_folder: str):
    for filename in os.listdir(input_folder):
        if not filename.endswith(".json"):
            continue
        print(f"processing data {filename}")
        file_path = os.path.join(input_folder, filename)
        python_filename = filename.split(".json")[0] + ".py"
        run_cmd_codegen(
            file_path,
            os.path.join(output_folder, python_filename),
            base_dofus_folder,
        )


def gen_map_datas(input_folder: str, output_folder: str):
    all_datas_groupes: dict = {"cellsData": {"Array": []}, "references": {"RefIds": []}}

    count = 0
    for filename in tqdm(os.listdir(input_folder)):
        if not filename.startswith("map_") or not filename.endswith(".json"):
            continue
        count += 1
        with open(os.path.join(input_folder, filename), "r+") as file:
            content = json.load(file)
        all_datas_groupes["cellsData"]["Array"].extend(content["cellsData"]["Array"])
        all_datas_groupes["references"]["RefIds"].extend(
            content["references"]["RefIds"]
        )
        if count > 500:
            break

    temp_path = "temp.json"
    with open(temp_path, "w+") as temp_file:
        json.dump(all_datas_groupes, temp_file, indent=2)
    output_file = os.path.join(output_folder, "MapsRoot.py")
    run_cmd_codegen(temp_path, output_file)
    os.remove(temp_path)


def gen_world_graph_datas(
    base_dofus_folder: str, input_folder: str, output_folder: str
):
    file_path = os.path.join(input_folder, WORLD_GRAPH_FILENAME)
    print("processing world graph")
    run_cmd_codegen(
        file_path,
        os.path.join(output_folder, "WorldGraphRoot" + ".py"),
        base_dofus_folder,
    )


def gen_all_python_class_datas():
    gen_datas(DOFUS_PATH, DOFUS_DATA_PATH, OUTPUT_CLASS_DATAS)
    gen_world_graph_datas(DOFUS_PATH, DOFUS_STANDALONE_PATH, OUTPUT_CLASS_STANDALONE)
    gen_map_datas(DOFUS_MAP_PATH, OUTPUT_CLASS_MAPS)


if __name__ == "__main__":
    gen_all_python_class_datas()
