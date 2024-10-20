from dataclasses import dataclass

from proto_schema_parser import Message

from db_dofus_unity.generator.comparator.models.proto_file_info import ProtoFileInfo


@dataclass
class ComparatorContextInfo:
    parent_context: "ComparatorContextInfo | None"  # to avoid infinite recursion
    file_info: ProtoFileInfo
    message: Message

    def get_depth_in_parent(self, msg_name: str) -> int | None:
        depth = 0
        is_found: bool = False
        context_info: ComparatorContextInfo | None = self
        while context_info is not None:
            depth += 1
            if context_info.message.name == msg_name:
                is_found = True
            context_info = context_info.parent_context

        if is_found:
            return depth
        return None
