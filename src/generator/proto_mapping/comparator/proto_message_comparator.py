from dataclasses import dataclass

from proto_schema_parser import Field
from proto_schema_parser.ast import (
    Message,
    MessageElement,
    OneOf,
    OneOfElement,
    FieldCardinality,
    Enum,
)

from src.generator.proto_mapping.comparator.consts import PROTO_BASE_FIELDS
from src.generator.proto_mapping.comparator.proto_enum_comparator import (
    ProtoEnumComparator,
)


@dataclass
class ProtoMessageInfo:
    parent_message_info: "ProtoMessageInfo | None"
    message: Message
    external_messages: dict[str, Message]
    external_enums: dict[str, Enum]

    def get_depth_in_parent(self, msg_name: str) -> int | None:
        depth = 0
        is_found: bool = False
        proto_msg_info: ProtoMessageInfo | None = self
        while proto_msg_info is not None:
            depth += 1
            if proto_msg_info.message.name == msg_name:
                is_found = True
            proto_msg_info = proto_msg_info.parent_message_info

        if is_found:
            return depth
        return None

    def get_available_messages(self):
        internal_messages = {
            element.name: element
            for element in self.message.elements
            if type(element) is Message
        }
        return self.external_messages | internal_messages

    def get_available_enums(self):
        internal_enums = {
            element.name: element
            for element in self.message.elements
            if type(element) is Enum
        }
        return self.external_enums | internal_enums


@dataclass
class ProtoMessageComparator:
    message_info_1: ProtoMessageInfo
    message_info_2: ProtoMessageInfo

    def compare(self) -> float:
        if len(self.message_info_1.message.elements) != len(
            self.message_info_2.message.elements
        ):
            return 0

        if len(self.message_info_1.message.elements) == 0:
            return 1

        self.message_info_1.message.elements.sort(
            key=lambda elem: self.get_sort_value_msg_element(elem)
        )
        self.message_info_2.message.elements.sort(
            key=lambda elem: self.get_sort_value_msg_element(elem)
        )

        elements_similarity_score: float = 0
        for index in range(len(self.message_info_1.message.elements)):
            msg_1_elem = self.message_info_1.message.elements[index]
            msg_2_elem = self.message_info_2.message.elements[index]
            elements_similarity_score += self.compare_msg_elements(
                msg_1_elem, msg_2_elem
            )

        return elements_similarity_score / len(self.message_info_1.message.elements)

    @staticmethod
    def get_sort_value_msg_element(msg_element: MessageElement) -> tuple:
        sort_by_type = str(type(msg_element))

        if type(msg_element) is Field:
            sort_by_field_value = msg_element.number
        else:
            sort_by_field_value = 0

        return sort_by_type, sort_by_field_value

    def compare_msg_elements(
        self, msg_element_1: MessageElement, msg_element_2: MessageElement
    ) -> float:
        if type(msg_element_1) is not type(msg_element_2):
            return 0

        if type(msg_element_1) is OneOf and type(msg_element_2) is OneOf:
            return self.compare_one_ofs(msg_element_1, msg_element_2)

        if type(msg_element_1) is Field and type(msg_element_2) is Field:
            return self.compare_fields(msg_element_1, msg_element_2)

        return 1

    def compare_one_ofs(self, one_of_1: OneOf, one_of_2: OneOf):
        if len(one_of_1.elements) != len(one_of_2.elements):
            return 0

        if len(one_of_1.elements) == 0:
            return 1

        elements_similarity_score: float = 0
        for index in range(len(one_of_1.elements)):
            sub_elem = one_of_1.elements[index]
            sub_elem2 = one_of_2.elements[index]
            elements_similarity_score += self.compare_one_of_element(
                sub_elem, sub_elem2
            )

        return elements_similarity_score / len(one_of_1.elements)

    def compare_one_of_element(
        self,
        one_of_element_1: OneOfElement,
        one_of_element_2: OneOfElement,
    ) -> float:
        if type(one_of_element_1) is not type(one_of_element_2):
            return 0

        if type(one_of_element_1) is Field and type(one_of_element_2) is Field:
            return self.compare_fields(one_of_element_1, one_of_element_2)

        return 1

    def compare_fields(self, field_1: Field, field_2: Field) -> float:
        similarity_score: float = 1
        coeff_check_failed: float = 1

        if field_1.number != field_2.number:
            coeff_check_failed += 1

        if field_1.type not in PROTO_BASE_FIELDS:
            if field_2.type in PROTO_BASE_FIELDS:
                return 0

            if related_enum_1 := self.message_info_1.get_available_enums().get(
                self.get_clean_type_name(field_1.type)
            ):
                related_enum_2 = self.message_info_2.get_available_enums().get(
                    self.get_clean_type_name(field_2.type)
                )
                if related_enum_2 is None:
                    return 0

                return ProtoEnumComparator(
                    enum_1=related_enum_1, enum_2=related_enum_2
                ).compare()

            if related_message_1 := self.message_info_1.get_available_messages().get(
                self.get_clean_type_name(field_1.type)
            ):
                related_message_2 = self.message_info_2.get_available_messages().get(
                    self.get_clean_type_name(field_2.type)
                )
                if related_message_2 is None:
                    return 0

                # TODO Vérifier any ca check pas correctement

                if (
                    depth_msg_info_1 := self.message_info_1.get_depth_in_parent(
                        related_message_1.name
                    )
                ) is not None:
                    if (
                        self.message_info_2.get_depth_in_parent(related_message_2.name)
                        == depth_msg_info_1
                    ):
                        return 1
                    return 0

                return ProtoMessageComparator(
                    message_info_1=ProtoMessageInfo(
                        parent_message_info=self.message_info_1,
                        message=related_message_1,
                        external_messages=self.message_info_1.external_messages,
                        external_enums=self.message_info_1.external_enums,
                    ),
                    message_info_2=ProtoMessageInfo(
                        parent_message_info=self.message_info_2,
                        message=related_message_2,
                        external_messages=self.message_info_2.external_messages,
                        external_enums=self.message_info_2.external_enums,
                    ),
                ).compare()

            return 1

        elif field_1.type != field_2.type:
            coeff_check_failed += 2

        if (field_1.cardinality == FieldCardinality.REPEATED) != (
            field_2.cardinality == FieldCardinality.REPEATED
        ):
            coeff_check_failed += 1

        return similarity_score / coeff_check_failed

    @staticmethod
    def get_clean_type_name(type_name: str):
        return type_name.split(".")[-1]
