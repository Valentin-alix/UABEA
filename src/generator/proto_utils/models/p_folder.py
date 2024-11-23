from dataclasses import dataclass
from functools import cache

from cachetools import cached

from src.generator.proto_utils.consts import PROTO_BASE_FIELDS, BLACKLIST_IMPORT_URLS
from src.generator.proto_utils.exceptions import TypeNotFound
from src.generator.proto_utils.models.p_enum import PEnum
from src.generator.proto_utils.models.p_file import PFile
from src.generator.proto_utils.models.p_message import (
    PMessage,
    PField,
    POneOf,
    PMapField,
)


@dataclass(frozen=True)
class PFolder:
    root: str
    files_by_filename: dict[str, PFile]

    def __hash__(self):
        return self.root.__hash__()

    @cached(
        cache={},
        key=lambda self, p_file, p_msg, stack: (self, p_file, p_msg),
    )
    def get_reliability_message(
        self, p_file: PFile, p_message: PMessage, p_stack_p_msg_id: set[int]
    ) -> float:
        p_stack_p_msg_id.add(id(p_message))
        value: float = 1
        for elem in p_message.elements:
            if type(elem) is PField:
                value += self.get_reliability_p_field(
                    p_file, p_message, elem, p_stack_p_msg_id
                )
            elif type(elem) is POneOf:
                for one_of_elem in elem.elements:
                    value += self.get_reliability_p_field(
                        p_file, p_message, one_of_elem, p_stack_p_msg_id
                    )
            elif type(elem) is PMapField:
                value += self.get_reliability_map_field(
                    p_file, p_message, elem, p_stack_p_msg_id
                )

        return value

    @cached(
        cache={},
        key=lambda self, p_file, p_msg, p_field, stack: (self, p_file, p_msg, p_field),
    )
    def get_reliability_p_field(
        self,
        p_file: PFile,
        p_message: PMessage,
        p_field: PField,
        p_stack_p_msg_id: set[int],
    ) -> float:
        if p_field.type_name in PROTO_BASE_FIELDS:
            return 1

        sub_msg_info = self.get_msg_or_enum_from_type_name(
            p_file, p_message, p_field.type_name
        )
        if not sub_msg_info:
            raise TypeNotFound(p_field.type_name)

        sub_p_file, sub_p_struct = sub_msg_info
        if type(sub_p_struct) is PMessage:
            if id(sub_p_struct) in p_stack_p_msg_id:
                return 1
            return self.get_reliability_message(
                sub_p_file, sub_p_struct, p_stack_p_msg_id
            )
        elif type(sub_p_struct) is PEnum:
            return sub_p_struct.reliability

        raise ValueError

    def get_reliability_map_field(
        self,
        p_file: PFile,
        p_message: PMessage,
        p_map_field: PMapField,
        p_stack_p_msg_id: set[int],
    ) -> float:
        reliability: float = 1

        reliability += self.get_reliability_p_field(
            p_file, p_message, p_map_field.value_p_field, p_stack_p_msg_id
        )

        return reliability

    @cache
    def get_msg_or_enum_from_type_name(
        self, p_file: PFile, p_message: PMessage, type_name: str
    ) -> tuple[PFile, PMessage | PEnum] | None:
        # search type inside msg
        prefix = f".{p_file.package}.{p_message.name}." if p_file.package else ""
        child_struct = p_message.get_msg_or_enum_inside_msg_from_type_name(
            prefix, type_name
        )
        if child_struct:
            return p_file, child_struct

        # search msg inside imported & current file
        for import_name in p_file.imports + [p_file.filename]:
            if import_name in BLACKLIST_IMPORT_URLS:
                continue
            imported_p_file = self.files_by_filename[import_name]
            imported_struct = (
                imported_p_file.get_msg_or_enum_inside_file_from_type_name(type_name)
            )
            if imported_struct:
                return imported_p_file, imported_struct

        return None
