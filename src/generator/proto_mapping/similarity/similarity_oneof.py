from proto_schema_parser.ast import OneOfElement, OneOf, Field

from src.generator.proto_mapping.similarity.similarity_field import compare_fields


def compare_one_of_elem(
    one_of_elem1: OneOfElement, one_of_elem2: OneOfElement
) -> float:
    if type(one_of_elem1) is not type(one_of_elem2):
        return 0

    if type(one_of_elem1) is Field and type(one_of_elem2) is Field:
        return compare_fields(one_of_elem1, one_of_elem2)


def compare_one_of_elems(
    one_of_elems1: list[OneOfElement], one_of_elems2: list[OneOfElement]
):
    if len(one_of_elems1) == 0:
        return 1

    elems_similarity_score: float = 0
    for index in range(len(one_of_elems1)):
        sub_elem = one_of_elems1[index]
        sub_elem2 = one_of_elems2[index]
        elems_similarity_score += compare_one_of_elem(sub_elem, sub_elem2)

    return elems_similarity_score / len(one_of_elems1)


def compare_one_ofs(one_of1: OneOf, one_of2: OneOf):
    if len(one_of1.elements) != len(one_of2.elements):
        return 0
    return compare_one_of_elems(one_of1.elements, one_of2.elements)
