from proto_schema_parser.ast import Enum, EnumValue

from src.generator.p_comparator.exceptions import UnhandledTypeCase
from src.generator.p_comparator.models.p_enum import PEnum, PEnumElement


class PEnumFactory:
    @staticmethod
    def create_p_enum(proto_enum: Enum) -> PEnum:
        p_enum_elements: list[PEnumElement] = []
        for elem in proto_enum.elements:
            if type(elem) is EnumValue:
                p_enum_elements.append(PEnumElement(name=elem.name, value=elem.number))
            else:
                raise UnhandledTypeCase(type(elem))
        return PEnum(name=proto_enum.name, elements=p_enum_elements)
