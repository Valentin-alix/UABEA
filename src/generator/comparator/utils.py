from proto_schema_parser.ast import MessageElement, Field, Package


def get_full_name_msg(package: Package | None, msg_name: str) -> str:
    if package:
        msg_full_name = package.name + "." + msg_name
    else:
        msg_full_name = msg_name

    return msg_full_name


def get_sort_value_msg_element(msg_element: MessageElement) -> tuple:
    sort_by_type = str(type(msg_element))

    if type(msg_element) is Field:
        sort_by_field_value = msg_element.number
    else:
        sort_by_field_value = 0

    return sort_by_type, sort_by_field_value
