from proto_schema_parser.ast import Enum


def get_enum_complexity(enum: Enum):
    complexity: float = 0
    for _ in enum.elements:
        complexity += 1
    return complexity
