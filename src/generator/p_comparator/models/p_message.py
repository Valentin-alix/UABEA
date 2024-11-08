from dataclasses import dataclass
from functools import cache

from proto_schema_parser.ast import FieldCardinality, MapField

from src.generator.p_comparator.models.p_enum import PEnum


@dataclass(frozen=True)
class PField:
    type_name: str
    name: str
    number: int
    cardinality: FieldCardinality | None

    def __hash__(self):
        return self.name.__hash__()


@dataclass(frozen=True)
class POneOf:
    name: str
    elements: list[PField]

    def __hash__(self):
        return self.name.__hash__()


@dataclass(frozen=True)
class PMessage:
    name: str
    elements: list[POneOf | PField | MapField]
    message_children: list["PMessage"]
    enum_children: list[PEnum]

    def __hash__(self):
        return self.name.__hash__()

    def __post_init__(self):
        self._sort_value_msg_element()

    @cache
    def get_msg_or_enum_inside_msg_from_type_name(
        self, prefix: str, type_name: str
    ) -> "PMessage|PEnum|None":
        """get related message for type name inside"""

        treated_msg: set[str] = set()
        stack: list[tuple[str, list[PMessage], list[PEnum]]] = [
            (prefix, self.message_children, self.enum_children)
        ]

        while stack:
            prefix, messages, enums = stack.pop(0)
            for enum in enums:
                if prefix + enum.name == type_name:
                    return enum

            for message in messages:
                if message.name in treated_msg:
                    continue
                treated_msg.add(message.name)

                full_msg_name = prefix + message.name
                if full_msg_name == type_name:
                    return message

                stack.append(
                    (
                        full_msg_name + ".",
                        message.message_children,
                        message.enum_children,
                    )
                )

        return None

    def _sort_value_msg_element(self) -> None:
        def get_sort_value_msg_element(msg_elem: PField | POneOf | MapField):
            sort_by_type = str(type(msg_elem))

            if type(msg_elem) is PField:
                sort_by_field_value = msg_elem.number
            else:
                sort_by_field_value = 0

            return sort_by_type, sort_by_field_value

        self.elements.sort(key=get_sort_value_msg_element)
