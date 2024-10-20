from dataclasses import dataclass

import icecream
from proto_schema_parser.ast import (
    MessageElement,
    Field,
    Message,
    OneOf,
    OneOfElement,
    Enum,
    EnumElement,
    EnumValue,
)

from db_dofus_unity.generator.comparator.consts import PROTO_BASE_FIELDS
from db_dofus_unity.generator.comparator.custom_types import Percentage
from db_dofus_unity.generator.comparator.models.comparator_context_info import (
    ComparatorContextInfo,
)
from db_dofus_unity.generator.comparator.models.mapping_info import MappingInfo
from db_dofus_unity.generator.comparator.models.proto_file_info import ProtoFileInfo
from db_dofus_unity.generator.comparator.utils import (
    get_sort_value_msg_element,
    get_related_struct,
)


@dataclass
class ProtoComparator:
    new_proto_files_infos: dict[str, ProtoFileInfo]
    old_proto_files_infos: dict[str, ProtoFileInfo]

    def get_most_probable_messages_mapping(self) -> dict[str, str]:
        mapping = self.get_messages_mapping()
        most_probable_matching: dict[str, str] = {}
        no_matching_founds: list[str] = []
        for new_msg_name, mapping_info in mapping.items():
            for old_msg_name in mapping_info.messages_name:
                if old_msg_name in most_probable_matching.values():
                    continue
                if mapping_info.similarity > 0.9:
                    most_probable_matching[new_msg_name] = old_msg_name
                else:
                    no_matching_founds.append(new_msg_name)
                break

        icecream.ic(no_matching_founds)

        return most_probable_matching

    def get_messages_mapping(self) -> dict[str, MappingInfo]:
        mapping_info_by_name: dict[str, MappingInfo] = {}

        for filename, new_proto_file_info in self.new_proto_files_infos.items():
            for new_message in new_proto_file_info.messages:
                mapping_info_by_name[new_message.name] = self.get_message_mapping(
                    new_proto_file_info, new_message
                )

        return mapping_info_by_name

    def get_message_mapping(
            self, new_proto_file_info: ProtoFileInfo, new_message: Message
    ) -> MappingInfo:
        mapping_by_sim: dict[str, float] = {}

        for old_proto_file_info in self.old_proto_files_infos.values():
            for old_message in old_proto_file_info.messages:
                old_comparator_info = ComparatorContextInfo(
                    file_info=old_proto_file_info,
                    message=old_message,
                    parent_context=None,
                )
                new_comparator_info = ComparatorContextInfo(
                    file_info=new_proto_file_info,
                    message=new_message,
                    parent_context=None,
                )
                mapping_by_sim[old_message.name] = self.compare_message(
                    old_comparator_info, new_comparator_info
                )

        most_sim = max(mapping_by_sim.values(), default=0.0)
        messages_name = [
            key for key, value in mapping_by_sim.items() if value == most_sim
        ]
        return MappingInfo(messages_name, similarity=most_sim)

    def compare_message(
            self,
            old_comparator_info: ComparatorContextInfo,
            new_comparator_info: ComparatorContextInfo,
    ) -> Percentage:
        if len(old_comparator_info.message.elements) != len(
                new_comparator_info.message.elements
        ):
            return 0

        if len(old_comparator_info.message.elements) == 0:
            return 1

        old_comparator_info.message.elements.sort(key=get_sort_value_msg_element)
        new_comparator_info.message.elements.sort(key=get_sort_value_msg_element)

        elements_similarity_score: float = 0
        for index in range(len(old_comparator_info.message.elements)):
            elements_similarity_score += self.compare_msg_elements(
                old_comparator_info,
                old_comparator_info.message.elements[index],
                new_comparator_info,
                new_comparator_info.message.elements[index],
            )

        return Percentage(
            elements_similarity_score / len(old_comparator_info.message.elements)
        )

    def compare_msg_elements(
            self,
            old_comparator_context: ComparatorContextInfo,
            old_msg_element: MessageElement,
            new_comparator_context: ComparatorContextInfo,
            new_msg_element: MessageElement,
    ) -> Percentage:
        if type(old_msg_element) is not type(new_msg_element):
            return 0

        if type(old_msg_element) is OneOf and type(new_msg_element) is OneOf:
            return self.compare_one_ofs(
                old_comparator_context,
                old_msg_element,
                new_comparator_context,
                new_msg_element,
            )

        if type(old_msg_element) is Field and type(new_msg_element) is Field:
            return self.compare_fields(
                old_comparator_context,
                old_msg_element,
                new_comparator_context,
                new_msg_element,
            )

        return 1

    def compare_one_ofs(
            self,
            old_comparator_context: ComparatorContextInfo,
            old_one_of: OneOf,
            new_comparator_context: ComparatorContextInfo,
            new_one_of: OneOf,
    ) -> Percentage:
        if len(old_one_of.elements) != len(new_one_of.elements):
            return 0

        if len(old_one_of.elements) == 0:
            return 1

        elements_similarity_score: float = 0
        for index in range(len(old_one_of.elements)):
            elements_similarity_score += self.compare_one_of_element(
                old_comparator_context,
                old_one_of.elements[index],
                new_comparator_context,
                new_one_of.elements[index],
            )

        return Percentage(elements_similarity_score / len(old_one_of.elements))

    def compare_one_of_element(
            self,
            old_comparator_context: ComparatorContextInfo,
            old_one_of_element: OneOfElement,
            new_comparator_context: ComparatorContextInfo,
            new_one_of_element: OneOfElement,
    ) -> Percentage:
        if type(old_one_of_element) is not type(new_one_of_element):
            return 0

        if type(old_one_of_element) is Field and type(new_one_of_element) is Field:
            return self.compare_fields(
                old_comparator_context,
                old_one_of_element,
                new_comparator_context,
                new_one_of_element,
            )

        return 1

    def compare_fields(
            self,
            old_comparator_context: ComparatorContextInfo,
            old_field: Field,
            new_comparator_context: ComparatorContextInfo,
            new_field: Field,
    ) -> Percentage:
        similarity_score: float = 1
        coeff_check_failed: float = 1

        if old_field.number != new_field.number:
            coeff_check_failed += 1

        cleaned_old_type = (
            old_field.type[1:] if old_field.type.startswith(".") else old_field.type
        )

        if cleaned_old_type not in PROTO_BASE_FIELDS:
            if new_field.type in PROTO_BASE_FIELDS:
                return 0

            related_old_struct_info = get_related_struct(
                self.old_proto_files_infos,
                old_comparator_context.file_info,
                old_comparator_context.message,
                old_field.type,
            )
            if related_old_struct_info is None:
                raise ValueError(f"Did not found struct {old_field.type}")

            related_old_file_info, related_old_struct = related_old_struct_info

            related_new_struct_info = get_related_struct(
                self.new_proto_files_infos,
                new_comparator_context.file_info,
                new_comparator_context.message,
                new_field.type,
            )

            if related_new_struct_info is None:
                raise ValueError(
                    f"Did not found struct {new_field.type} at file info {new_comparator_context}"
                )
            related_new_file_info, related_new_struct = related_new_struct_info

            if (
                    type(related_old_struct) is Message
                    and type(related_new_struct) is Message
            ):
                old_depth = old_comparator_context.get_depth_in_parent(
                    related_old_struct.name
                )
                # to avoid infinite recursion
                if old_depth is not None:
                    new_depth = new_comparator_context.get_depth_in_parent(
                        related_new_struct.name
                    )
                    if new_depth == old_depth:
                        return 1
                    return 0

                return self.compare_message(
                    ComparatorContextInfo(
                        file_info=related_old_file_info,
                        message=related_old_struct,
                        parent_context=old_comparator_context,
                    ),
                    ComparatorContextInfo(
                        file_info=related_new_file_info,
                        message=related_new_struct,
                        parent_context=new_comparator_context,
                    ),
                )

            if type(related_old_struct) is Enum and type(related_new_struct) is Enum:
                return ProtoComparator.compare_enum(
                    related_old_struct, related_new_struct
                )

            return 0

        elif cleaned_old_type != new_field.type:
            coeff_check_failed += 2

        if old_field.cardinality != new_field.cardinality:
            coeff_check_failed += 1

        return Percentage(similarity_score / coeff_check_failed)

    @staticmethod
    def compare_enum(old_enum: Enum, new_enum: Enum) -> Percentage:
        if len(old_enum.elements) != len(new_enum.elements):
            return 0

        elements_similarity_score: float = 0
        for index in range(len(old_enum.elements)):
            old_enum_element = old_enum.elements[index]
            new_enum_element = new_enum.elements[index]
            elements_similarity_score += ProtoComparator.compare_enum_element(
                old_enum_element, new_enum_element
            )

        return Percentage(elements_similarity_score / len(old_enum.elements))

    @staticmethod
    def compare_enum_element(
            old_enum_element: EnumElement, new_enum_element: EnumElement
    ) -> Percentage:
        if type(old_enum_element) is not type(new_enum_element):
            return 0

        similarity_score: float = 1
        coeff_check_failed: float = 1
        if type(old_enum_element) is EnumValue and type(new_enum_element) is EnumValue:
            if old_enum_element.number != new_enum_element.number:
                coeff_check_failed += 2
            if old_enum_element.name != new_enum_element.name:
                coeff_check_failed += 1

        return Percentage(similarity_score / coeff_check_failed)
