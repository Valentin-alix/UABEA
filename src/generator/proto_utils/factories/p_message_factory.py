from dataclasses import dataclass

from proto_schema_parser import Message, Field
from proto_schema_parser.ast import OneOf, Enum, MapField

from src.generator.proto_utils.exceptions import UnhandledTypeCase
from src.generator.proto_utils.factories.p_enum_factory import PEnumFactory
from src.generator.proto_utils.models.p_enum import PEnum
from src.generator.proto_utils.models.p_message import (
    PMessage,
    POneOf,
    PField,
    PMapField,
)


class PMessageFactory:
    @staticmethod
    def create_p_message(proto_message: Message) -> PMessage:
        p_message_elements: list[POneOf | PField | PMapField] = []
        p_message_children: list[PMessage] = []
        p_enum_children: list[PEnum] = []
        for elem in proto_message.elements:
            if type(elem) is Field:
                p_message_elements.append(
                    PField(
                        type_name=elem.type,
                        name=elem.name,
                        number=elem.number,
                        cardinality=elem.cardinality,
                    )
                )
            elif type(elem) is OneOf:
                p_message_elements.append(POneOfFactory.create_p_one_of(elem))
            elif type(elem) is Message:
                p_message_children.append(PMessageFactory.create_p_message(elem))
            elif type(elem) is Enum:
                p_enum_children.append(PEnumFactory.create_p_enum(elem))
            elif type(elem) is MapField:
                p_message_elements.append(PMapFieldFactory.create_p_map_field(elem))
            else:
                raise UnhandledTypeCase(type(elem))

        return PMessage(
            name=proto_message.name,
            elements=p_message_elements,
            message_children=p_message_children,
            enum_children=p_enum_children,
        )


@dataclass
class POneOfFactory:
    @staticmethod
    def create_p_one_of(proto_one_of: OneOf) -> POneOf:
        p_one_of_elements: list[PField] = []
        for elem in proto_one_of.elements:
            if type(elem) is Field:
                p_one_of_elements.append(
                    PField(
                        type_name=elem.type,
                        name=elem.name,
                        number=elem.number,
                        cardinality=elem.cardinality,
                    )
                )
            else:
                raise UnhandledTypeCase(type(elem))
        return POneOf(name=proto_one_of.name, elements=p_one_of_elements)


class PMapFieldFactory:
    @staticmethod
    def create_p_map_field(map_field: MapField) -> PMapField:
        value_p_field = PField(
            type_name=map_field.value_type,
            name=map_field.name,
            number=map_field.number,
            cardinality=None,
        )
        return PMapField(key_type=map_field.key_type, value_p_field=value_p_field)
