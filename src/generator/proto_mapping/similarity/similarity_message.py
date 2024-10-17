from proto_schema_parser import Field
from proto_schema_parser.ast import Message, MessageElement, OneOf


def compare_similary_msg_element(msg_elem1: MessageElement, msg_elem2: MessageElement):
    if type(msg_elem1) is not type(msg_elem2):
        return False

    if type(msg_elem1) is Field and type(msg_elem2) is Field:
        if msg_elem1.number != msg_elem2.number:
            return False

    elif isinstance(msg_elem1, OneOf) and isinstance(msg_elem2, OneOf):
        if len(msg_elem1.elements) != len(msg_elem2.elements):
            return False

        for index in range(len(msg_elem1.elements)):
            sub_msg1_elem = msg_elem1.elements[index]
            sub_msg2_elem = msg_elem2.elements[index]
            if not compare_similary_msg_element(sub_msg1_elem, sub_msg2_elem):
                return False

    return True


def compare_similarity_message(msg1: Message, msg2: Message):
    if len(msg1.elements) != len(msg2.elements):
        return False
    msg1.elements.sort(key=lambda elem: str(type(elem)))
    msg2.elements.sort(key=lambda elem: str(type(elem)))
    for index in range(len(msg1.elements)):
        msg1_elem = msg1.elements[index]
        msg2_elem = msg2.elements[index]
        if not compare_similary_msg_element(msg1_elem, msg2_elem):
            return False

    return True
