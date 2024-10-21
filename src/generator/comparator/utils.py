from proto_schema_parser.ast import MessageElement, Field, Message, Enum

from src.generator.comparator.models.proto_file_info import ProtoFileInfo


def get_sort_value_msg_element(msg_element: MessageElement) -> tuple:
    sort_by_type = str(type(msg_element))

    if type(msg_element) is Field:
        sort_by_field_value = msg_element.number
    else:
        sort_by_field_value = 0

    return sort_by_type, sort_by_field_value


def get_related_struct(
    proto_file_info_by_filename: dict[str, ProtoFileInfo],
    proto_file_info: ProtoFileInfo,
    from_msg: Message,
    type_name: str,
) -> tuple[ProtoFileInfo, Message | Enum] | None:
    if struct := find_struct_inside_message_by_type_name(from_msg, "", type_name):
        # search inside message
        return proto_file_info, struct

    reachable_files_infos: list[ProtoFileInfo] = [
        proto_file_info_by_filename[proto_import.name]
        for proto_import in proto_file_info.imports
        if proto_import.name in proto_file_info_by_filename
    ]
    reachable_files_infos.append(proto_file_info)

    for reachable_file_info in reachable_files_infos:
        prefix = (
            f".{reachable_file_info.package.name}."
            if reachable_file_info.package
            else ""
        )

        for sub_message in reachable_file_info.messages:
            sub_msg_full_name = prefix + sub_message.name
            if sub_msg_full_name == type_name:
                return reachable_file_info, sub_message
            if struct := find_struct_inside_message_by_type_name(
                sub_message, prefix + sub_message.name + ".", type_name
            ):
                return reachable_file_info, struct

        for enum in reachable_file_info.enums:
            enum_full_name = prefix + enum.name
            if enum_full_name == type_name:
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
