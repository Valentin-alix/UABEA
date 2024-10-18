from proto_schema_parser import Field
from proto_schema_parser.ast import Message, MessageElement, OneOf, OneOfElement, Enum

from src.generator.proto_mapping.similarity.similarity_enum import compare_enums
from src.generator.proto_mapping.similarity.similarity_field import compare_fields
from src.generator.proto_mapping.similarity.similarity_oneof import compare_one_ofs


def compare_msg_elements(msg_elem1: MessageElement, msg_elem2: MessageElement) -> float:
    if type(msg_elem1) is not type(msg_elem2):
        return 0

    if type(msg_elem1) is Field and type(msg_elem2) is Field:
        return compare_fields(msg_elem1, msg_elem2)

    if type(msg_elem1) is OneOf and type(msg_elem2) is OneOf:
        return compare_one_ofs(msg_elem1, msg_elem2)

    return 1


def get_sort_value_msg_elem(msg_elem: MessageElement):
    sort_by_type = str(type(msg_elem))

    if type(msg_elem) is Field:
        sort_by_field_value = msg_elem.number
    else:
        sort_by_field_value = 0

    return sort_by_type, sort_by_field_value


def compare_messages(msg1: Message, msg2: Message) -> float:
    if len(msg1.elements) != len(msg2.elements):
        return 0

    if len(msg1.elements) == 0:
        return 1

    msg1.elements.sort(key=lambda elem: get_sort_value_msg_elem(elem))
    msg2.elements.sort(key=lambda elem: get_sort_value_msg_elem(elem))

    elems_similarity_score: float = 0
    for index in range(len(msg1.elements)):
        msg1_elem = msg1.elements[index]
        msg2_elem = msg2.elements[index]
        elems_similarity_score += compare_msg_elements(msg1_elem, msg2_elem)

    return elems_similarity_score / len(msg1.elements)
