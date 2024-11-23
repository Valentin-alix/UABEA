import importlib.util
import re
import sys


def to_snake_case(value: str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def instantiate_class_from_path(class_name: str, file_path: str) -> type[object]:
    spec = importlib.util.spec_from_file_location(class_name, file_path)
    if spec is None:
        raise FileNotFoundError
    module = importlib.util.module_from_spec(spec)
    sys.modules[class_name] = module
    spec.loader.exec_module(module)  # type: ignore

    cls = getattr(module, class_name)

    return cls


if __name__ == "__main__":
    _type = instantiate_class_from_path(
        "Model",
        "D:\\Workspace\\DB-DofusUnity\\db_dofus_unity\\models\\datas\\AbuseReasonsRoot.py",
    )
    print(_type)
