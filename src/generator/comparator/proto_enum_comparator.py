from dataclasses import dataclass

from proto_schema_parser.ast import Enum, EnumElement, EnumValue


@dataclass
class ProtoEnumComparator:
    enum_1: Enum
    enum_2: Enum

    def compare(self) -> float:
        if len(self.enum_1.elements) != len(self.enum_2.elements):
            return 0

        elements_similarity_score: float = 0
        for index in range(len(self.enum_1.elements)):
            enum_1_element = self.enum_1.elements[index]
            enum_2_element = self.enum_2.elements[index]
            elements_similarity_score += self.compare_enum_elements(
                enum_1_element, enum_2_element
            )

        return elements_similarity_score / len(self.enum_1.elements)

    @staticmethod
    def compare_enum_elements(
        enum_elem_1: EnumElement, enum_elem_2: EnumElement
    ) -> float:
        if type(enum_elem_1) is not type(enum_elem_2):
            return 0

        similarity_score: float = 1
        coeff_check_failed: float = 1
        if type(enum_elem_1) is EnumValue and type(enum_elem_2) is EnumValue:
            if enum_elem_1.number != enum_elem_2.number:
                coeff_check_failed += 2
            if enum_elem_1.name != enum_elem_2.name:
                coeff_check_failed += 1

        return similarity_score / coeff_check_failed
