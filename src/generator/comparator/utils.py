from proto_schema_parser.ast import MessageElement, Field, Message, Enum, OneOf

from src.generator.comparator.consts import PROTO_BASE_FIELDS
from src.generator.comparator.models.message_context_info import MessageContextInfo
from src.generator.comparator.models.proto_file_info import ProtoFileInfo


def get_sort_value_msg_element(msg_element: MessageElement) -> tuple:
    sort_by_type = str(type(msg_element))

    if type(msg_element) is Field:
        sort_by_field_value = msg_element.number
    else:
        sort_by_field_value = 0

    return sort_by_type, sort_by_field_value


def get_complexity_msg_elem(
    msg_elem: MessageElement, proto_file_info_by_filename: dict[str, ProtoFileInfo]
):
    if type(msg_elem) is OneOf:
        complexity_one_of: int = 0
        for one_of_elem in msg_elem.elements:
            complexity_one_of += get_complexity_msg_elem(
                one_of_elem, proto_file_info_by_filename
            )
        return complexity_one_of
    elif type(msg_elem) is Field:
        cleaned_old_type = (
            msg_elem.type[1:] if msg_elem.type.startswith(".") else msg_elem.type
        )
        if cleaned_old_type in PROTO_BASE_FIELDS:
            return 1
        else:
            return 2
        # related_old_struct_info = get_related_struct(
        #     proto_file_info_by_filename,
        #     context_info,
        #     msg_elem.type,
        # )
        # msg_elem_context = MessageContextInfo(parent_context=context_info, file_info=context_info.file_info,
        #                                       message=msg_elem)
        # if not related_old_struct_info:
        #     print(f"did not found {msg_elem.type}")
        #     return 0
        # related_file_info, related_struct = related_old_struct_info
        # if type(related_struct) is Enum:
        #     return len(related_struct.elements)
        # elif type(related_struct) is Message:
        #     return get_complexity_struct(proto_file_info_by_filename, context_info, related_struct)

    return 0


def get_complexity_struct(
    proto_file_info_by_filename: dict[str, ProtoFileInfo], msg: Message
):
    complexity: int = 0
    for msg_elem in msg.elements:
        complexity += get_complexity_msg_elem(msg_elem, proto_file_info_by_filename)

    return complexity


def get_related_struct(
    proto_file_info_by_filename: dict[str, ProtoFileInfo],
    context_info: MessageContextInfo,
    target_type_name: str,
) -> tuple[ProtoFileInfo, Message | Enum] | None:
    """
    proto_file_info_by_filename: the context containing all available files infos
    """
    if struct := find_struct_inside_message_by_type_name(
        context_info.message, "", target_type_name
    ):
        # search inside message
        return context_info.file_info, struct

    reachable_files_infos: list[ProtoFileInfo] = [
        proto_file_info_by_filename[proto_import.name]
        for proto_import in context_info.file_info.imports
        if proto_import.name in proto_file_info_by_filename
    ]
    reachable_files_infos.append(context_info.file_info)

    for reachable_file_info in reachable_files_infos:
        prefix = (
            f".{reachable_file_info.package.name}."
            if reachable_file_info.package
            else ""
        )

        for sub_message in reachable_file_info.messages:
            sub_msg_full_name = prefix + sub_message.name
            if sub_msg_full_name == target_type_name:
                return reachable_file_info, sub_message
            if struct := find_struct_inside_message_by_type_name(
                sub_message, prefix + sub_message.name + ".", target_type_name
            ):
                return reachable_file_info, struct

        for enum in reachable_file_info.enums:
            enum_full_name = prefix + enum.name
            if enum_full_name == target_type_name:
                return reachable_file_info, enum

    return None


def find_struct_inside_message_by_type_name(
    message: Message, prefix: str, type_name: str
) -> Message | Enum | None:
    for struct_elem in message.elements:
        if type(struct_elem) is Message or type(struct_elem) is Enum:
            full_name_msg_elem = prefix + struct_elem.name
            if full_name_msg_elem == type_name:
                return struct_elem

        if type(struct_elem) is Message:
            sub_struct = find_struct_inside_message_by_type_name(
                struct_elem, prefix + f"{struct_elem.name}.", type_name
            )
            if sub_struct:
                return sub_struct

    return None
