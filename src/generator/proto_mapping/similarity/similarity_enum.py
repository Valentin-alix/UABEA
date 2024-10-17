from proto_schema_parser.ast import Enum, EnumElement, EnumValue


def compare_similary_enum_element(enum_elem1: EnumElement, enum_elem2: EnumElement):
    if type(enum_elem1) is not type(enum_elem2):
        return False

    if type(enum_elem1) is EnumValue and type(enum_elem2) is EnumValue:
        if enum_elem1.number != enum_elem2.number:
            return False
        if enum_elem1.name != enum_elem2.name:
            print(enum_elem1.name, enum_elem2.name)
            return False

    return True


def compare_similarity_enum(enum1: Enum, enum2: Enum):
    if len(enum1.elements) != len(enum2.elements):
        return False
    for index in range(len(enum1.elements)):
        enum1_elem = enum1.elements[index]
        enum2_elem = enum2.elements[index]
        if not compare_similary_enum_element(enum1_elem, enum2_elem):
            return False

    return True
