import json
import os
from collections import defaultdict
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import cast

import msgspec.json
from msgspec import Struct
from tqdm import tqdm

from D3Database.consts import (
    WORLD_GRAPH_FILENAME,
    D3_DATABASE,
    D3_DATA,
    OUTPUT_CLASS_DATAS,
    D3_STANDALONE,
    OUTPUT_CLASS_STANDALONE,
    D3_MAP,
    OUTPUT_CLASS_MAPS,
)
from src.utils import instantiate_class_from_path


def run_cmd_codegen(
    input_filename: str,
    output_filename: str,
    base_folder: str | None = None,
    excluded_field_by_class_name: dict[str, list[str]] | None = None,
    excluded_class_name: list[str] | None = None,
) -> None:
    cmd = (
        f"datamodel-codegen --input-file-type json --input {input_filename} --output {output_filename} --custom"
        f"-template-dir {os.path.join(Path(__file__).parent, "template")}  --output-model-type msgspec.Struct "
        f"--encoding utf-8"
    )
    extra_data: dict[str, dict] = defaultdict(dict)
    if base_folder is not None:
        filepath = os.path.relpath(input_filename, base_folder)
        extra_data["Model"]["filepath"] = filepath

    if excluded_field_by_class_name:
        for class_name, excluded_fields in excluded_field_by_class_name.items():
            extra_data[class_name]["excluded_fields"] = excluded_fields
    if excluded_class_name:
        for class_name in excluded_class_name:
            extra_data[class_name]["excluded_model"] = True
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
            file_path,
            os.path.join(output_folder, python_filename),
            base_folder,
            excluded_field_by_class_name={
                "Model": [
                    "m_GameObject",
                    "m_Enabled",
                    "m_Script",
                    "m_Name",
                    "objectsById",
                ],
                "References": ["version"],
                "RefId": ["rid", "type"],
            },
            excluded_class_name=["MScript", "MGameObject", "ObjectsById", "Type"],
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


def gen_and_clean_map_datas(input_folder: str, output_folder: str):
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
        if count > 100:
            break

    temp_path = "unity_output.json"
    with open(temp_path, "w+") as temp_file:
        json.dump(all_datas_groupes, temp_file, indent=2)
    output_file = os.path.join(output_folder, "MapsRoot.py")
    run_cmd_codegen(
        temp_path,
        output_file,
        excluded_field_by_class_name={
            "RefId": ["rid", "type"],
            "Data": [
                "color",
                "transform",
                "materialIndex",
                "innerCellRenderOrder",
                "displayBehaviour",
                "shaderParameters",
                "unique",
                "stagingId",
                "paintSpanOrder",
                "background",
                "playAnimation",
                "playAnimStatic",
                "minDelay",
                "maxDelay",
                "requiresServerUpdate",
                "paintSpanOrder",
                "type",
                "animationCurveType",
                "finalColor",
                "frequency",
                "linkFrequencyToWind",
                "timeOffset",
                "isTimeOffsetRandom",
                "shouldSmooth",
                "shouldApplyNoise",
                "noiseTexID",
                "noiseOffset",
                "isNoiseOffsetRandom",
                "noiseStrength",
                "linkNoiseStrengthToWind",
                "noiseSpeed",
                "linkNoiseSpeedToWind",
                "dissolveTexID",
                "dissolveTexTiling",
                "dissolveTexOffset",
                "isDissolveTexOffsetRandom",
                "dissolveTexSpeed",
                "texSpeedMultiplier",
                "isTexSpeedMultiplierRandom",
                "texSpeedMultiplierRandomRatio",
                "dissolveMaskID",
                "alphaClip",
                "alphaClipFadeWidth",
                "burnColor",
                "burnColorPower",
                "burnWidth",
                "isBurnFaded",
                "displayUseDissolvePerParticle",
                "useDissolvePerParticle",
                "alphaClipPerParticle",
                "isAnimated",
                "curveMin",
                "curveMax",
                "isAnimated",
                "noiseTexUVMode",
                "noiseTexTiling",
                "tile",
                "noiseTexOffset",
                "strength",
                "direction",
                "directionSpeedMultiplier",
                "isDirectionSpeedMultiplierRandom",
                "directionSpeedMultiplierRandomRatio",
                "linkToWind",
                "maskTexID",
                "sourceFactor",
                "blendOperation",
                "destinationFactor",
                "isWindSensitive",
                "bendCenter",
                "worldSpaceBendCenter",
                "bendStart",
                "worldSpaceBendStart",
                "bendAxe",
                "bendAxeMultiplier",
                "flexibility",
                "shouldSwing",
                "windSwingNoiseSpeedCoef",
                "windSwingNoiseAmplitude",
                "parentParameters",
                "rotationCenter",
                "amplitude",
                "linkAmplitudeToWind",
                "offset",
                "emissiveTexID",
                "factor",
                "displayUseEmissiveAnimationPerParticle",
                "useEmissiveAnimationPerParticle",
                "animationOffsetPerParticle",
                "curveClampMin",
                "curveClampMax",
                "isFrequencyNoised",
                "frequencyNoiseTexID",
                "areAreasDelayed",
                "axes",
                "pivot",
                "noiseStrengthMultiplier",
                "threshold",
                "intensity",
                "scatter",
                "textureOffsetType",
                "texUVMode",
                "texTiling",
                "texOffset",
                "directionSpeed",
                "flowmapID",
                "flowmapSpeed",
                "flowmapPower",
            ],
        },
        excluded_class_name=["MScript", "MGameObject", "ObjectsById", "Type"],
    )
    os.remove(temp_path)

    print("cleaning map folder..")
    class_type = cast(Struct, instantiate_class_from_path("Model", output_file))
    for filename in tqdm(os.listdir(input_folder)):
        if not filename.startswith("map_") or not filename.endswith(".json"):
            continue
        file_path = os.path.join(input_folder, filename)
        with open(file_path, "rb") as file:
            content = msgspec.json.decode(file.read(), type=class_type)
        with open(file_path, "wb") as file:
            file.write(msgspec.json.encode(content))


def gen_and_clean_world_graph_datas(
    base_folder: str, input_folder: str, output_folder: str
):
    file_path = os.path.join(input_folder, WORLD_GRAPH_FILENAME)
    print("processing world graph")
    run_cmd_codegen(
        file_path,
        os.path.join(output_folder, "WorldGraphRoot" + ".py"),
        base_folder,
        excluded_field_by_class_name={
            "Model": [
                "m_GameObject",
                "m_Enabled",
                "m_Script",
                "m_Name",
            ],
        },
        excluded_class_name=["MScript", "MGameObject", "ObjectsById", "Type"],
    )

    print("cleaning world graph")
    class_type = cast(
        Struct,
        instantiate_class_from_path(
            "Model",
            os.path.join(output_folder, "WorldGraphRoot" + ".py"),
        ),
    )
    with open(file_path, "rb") as file:
        content: Struct = msgspec.json.decode(file.read(), type=class_type)
    with open(file_path, "wb") as file:
        file.write(msgspec.json.format(msgspec.json.encode(content), indent=2))


def gen_and_clean_python_class_datas():
    gen_and_clean_datas(D3_DATABASE, D3_DATA, OUTPUT_CLASS_DATAS)
    gen_and_clean_world_graph_datas(D3_DATABASE, D3_STANDALONE, OUTPUT_CLASS_STANDALONE)
    gen_and_clean_map_datas(D3_MAP, OUTPUT_CLASS_MAPS)


if __name__ == "__main__":
    gen_and_clean_python_class_datas()
