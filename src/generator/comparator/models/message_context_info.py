from dataclasses import dataclass

from proto_schema_parser import Message
from proto_schema_parser.ast import Enum, MessageElement, OneOf, Field

from src.generator.comparator.consts import BLACKLIST_IMPORT_URLS, PROTO_BASE_FIELDS
from src.generator.comparator.models.proto_file_info import ProtoFileInfo


@dataclass
class MessageContextInfo:
    file_info_by_name: dict[str, ProtoFileInfo]
    parent_context: "MessageContextInfo | None"  # to avoid infinite recursion
    file_info: ProtoFileInfo
    message: Message

    def get_msg_info_or_enum_from_type_name(
        self, type_name: str
    ) -> "MessageContextInfo | Enum | None":
        if self.file_info.package is None and (
            reachable_sub_struct := self.find_struct_inside_msg_by_type_name(
                self.message, "", type_name
            )
        ):  # search inside message
            if type(reachable_sub_struct) is Enum:
                return reachable_sub_struct

            if type(reachable_sub_struct) is Message:
                msg_info = MessageContextInfo(
                    file_info_by_name=self.file_info_by_name,
                    message=reachable_sub_struct,
                    file_info=self.file_info,
                    parent_context=self,
                )
                return msg_info

        reachable_files_infos: list[ProtoFileInfo] = [
            self.file_info_by_name[proto_import.name]
            for proto_import in self.file_info.imports
            if proto_import.name not in BLACKLIST_IMPORT_URLS
        ]
        reachable_files_infos.append(self.file_info)

        for reachable_file_info in reachable_files_infos:
            prefix = (
                f".{reachable_file_info.package.name}."
                if reachable_file_info.package
                else ""
            )
            for reachable_msg in reachable_file_info.messages:
                reachable_msg_with_prefix = prefix + reachable_msg.name
                if reachable_msg_with_prefix == type_name:
                    reachable_msg_info = MessageContextInfo(
                        file_info_by_name=self.file_info_by_name,
                        parent_context=self,
                        file_info=reachable_file_info,
                        message=reachable_msg,
                    )
                    return reachable_msg_info

                if reachable_sub_struct := self.find_struct_inside_msg_by_type_name(
                    reachable_msg, prefix + reachable_msg.name + ".", type_name
                ):
                    if type(reachable_sub_struct) is Enum:
                        return reachable_sub_struct

                    if type(reachable_sub_struct) is Message:
                        reachable_sub_msg_info = MessageContextInfo(
                            file_info_by_name=self.file_info_by_name,
                            parent_context=self,
                            file_info=reachable_file_info,
                            message=reachable_sub_struct,
                        )
                        return reachable_sub_msg_info

            for reachable_enum in reachable_file_info.enums:
                enum_name_with_prefix = prefix + reachable_enum.name
                if enum_name_with_prefix == type_name:
                    return reachable_enum

        return None

    def find_struct_inside_msg_by_type_name(
        self, message: Message, prefix: str, type_name: str
    ) -> Message | Enum | None:
        for msg_elem in message.elements:

            if not type(msg_elem) is Message and not type(msg_elem) is Enum:
                continue

            msg_name_with_prefix = prefix + msg_elem.name
            if msg_name_with_prefix == type_name:
                return msg_elem

            if not type(msg_elem) is Message:
                continue
            sub_msg = self.find_struct_inside_msg_by_type_name(
                msg_elem, prefix + f"{msg_elem.name}.", type_name
            )
            if sub_msg:
                return sub_msg

        return None

    def get_complexity(self) -> int:
        complexity: int = 0
        for msg_elem in self.message.elements:
            complexity += self.get_complexity_msg_elem(msg_elem)
        return complexity

    def get_complexity_msg_elem(self, msg_elem: MessageElement) -> int:
        if type(msg_elem) is OneOf:
            complexity_one_of: int = 0
            for one_of_elem in msg_elem.elements:
                complexity_one_of += self.get_complexity_msg_elem(one_of_elem)
            return complexity_one_of
        elif type(msg_elem) is Field:
            cleaned_old_type = (
                msg_elem.type[1:] if msg_elem.type.startswith(".") else msg_elem.type
            )
            if cleaned_old_type in PROTO_BASE_FIELDS:
                return 1

            related_struct_info = self.get_msg_info_or_enum_from_type_name(
                msg_elem.type
            )
            if type(related_struct_info) is Enum:
                return len(related_struct_info.elements)

            if type(related_struct_info) is MessageContextInfo:
                if (
                    self.get_depth_in_parent(related_struct_info.message.name)
                    is not None
                ):
                    return 1
                complexity_sub_msg: int = 0
                for msg_elem in related_struct_info.message.elements:
                    complexity_sub_msg += related_struct_info.get_complexity_msg_elem(
                        msg_elem
                    )
                return complexity_sub_msg

        return 0

    def get_depth_in_parent(self, msg_name: str) -> int | None:
        """search message context info by msg name in parents and return depth of parent"""
        depth = 0
        is_found: bool = False
        context_info: MessageContextInfo | None = self
        while context_info is not None:
            depth += 1
            if context_info.message.name == msg_name:
                is_found = True
            context_info = context_info.parent_context

        if is_found:
            return depth
        return None
