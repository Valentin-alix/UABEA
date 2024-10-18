from src.generator.proto_mapping.complexity.enum_complexity import get_enum_complexity


from proto_schema_parser.ast import Enum, Message


def get_msg_complexity(msg: Message):
    complexity: float = 0
    for elem in msg.elements:
        complexity += 1
        if type(elem) is Message:
            complexity += get_msg_complexity(elem)
        if type(elem) is Enum:
            complexity += get_enum_complexity(elem)

    return complexity
