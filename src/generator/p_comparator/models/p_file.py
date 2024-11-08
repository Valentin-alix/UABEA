from dataclasses import dataclass
from functools import cache

from src.generator.p_comparator.models.p_enum import PEnum
from src.generator.p_comparator.models.p_message import PMessage


@dataclass(frozen=True)
class PFile:
    filename: str
    package: str | None
    imports: list[str]
    messages: list[PMessage]
    enums: list[PEnum]

    def __hash__(self):
        return self.filename.__hash__()

    @cache
    def get_msg_or_enum_inside_file_from_type_name(
        self, type_name: str
    ) -> "PMessage|PEnum|None":
        prefix: str
        if self.package:
            prefix = f".{self.package}."
        else:
            prefix = ""

        for message in self.messages:
            full_msg_name = prefix + message.name
            if full_msg_name == type_name:
                return message
            child_msg = message.get_msg_or_enum_inside_msg_from_type_name(
                full_msg_name + ".", type_name
            )
            if child_msg:
                return child_msg

        for enum in self.enums:
            full_msg_name = prefix + enum.name
            if full_msg_name == type_name:
                return enum

        return None
