from proto_schema_parser.ast import Enum, EnumElement, EnumValue


def compare_enum_elements(enum_elem1: EnumElement, enum_elem2: EnumElement) -> float:
    if type(enum_elem1) is not type(enum_elem2):
        return 0

    similarity_score: float = 1
    coeff_check_failed: float = 1
    if type(enum_elem1) is EnumValue and type(enum_elem2) is EnumValue:
        if enum_elem1.number != enum_elem2.number:
            coeff_check_failed += 2
        if enum_elem1.name != enum_elem2.name:
            coeff_check_failed += 1

    return similarity_score / coeff_check_failed


def compare_enums(enum1: Enum, enum2: Enum) -> float:
    if len(enum1.elements) != len(enum2.elements):
        return 0

    elems_similarity_score: float = 0
    for index in range(len(enum1.elements)):
        enum1_elem = enum1.elements[index]
        enum2_elem = enum2.elements[index]
        elems_similarity_score += compare_enum_elements(enum1_elem, enum2_elem)

    return elems_similarity_score / len(enum1.elements)
