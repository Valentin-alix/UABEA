import re


def to_snake_case(value: str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()
