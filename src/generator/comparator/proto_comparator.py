from copy import deepcopy
from dataclasses import dataclass

from proto_schema_parser.ast import (
    MessageElement,
    Field,
    Message,
    OneOf,
    OneOfElement,
    Enum,
    EnumElement,
    EnumValue,
    Package,
)

from src.generator.comparator.consts import PROTO_BASE_FIELDS
from src.generator.comparator.custom_types import Percentage
from src.generator.comparator.models.mapping_info import MappingInfo
from src.generator.comparator.models.message_context_info import (
    MessageContextInfo,
)
from src.generator.comparator.models.proto_file_info import ProtoFileInfo
from src.generator.comparator.utils import (
    get_sort_value_msg_element,
    get_related_struct,
    get_complexity_struct,
)


@dataclass
class ProtoComparator:
    new_proto_files_infos: dict[str, ProtoFileInfo]
    old_proto_files_infos: dict[str, ProtoFileInfo]

    def get_full_name_msg(self, package: Package | None, name: str) -> str:
        if package:
            msg_full_name = package.name + "." + name
        else:
            msg_full_name = name

        return msg_full_name

    def get_all_messages_mapping(self) -> dict[str, MappingInfo]:
        mapping_info_by_name: dict[str, MappingInfo] = {}

        # deepcopy to keep context for retrieving element but to get rid of matching possibility
        new_proto_files_infos = deepcopy(self.new_proto_files_infos)

        # here we sort proto file by most complex msg
        old_proto_files_infos_sorted_complexity = sorted(
            self.old_proto_files_infos.items(),
            key=lambda item: max(
                (
                    get_complexity_struct(self.old_proto_files_infos, msg)
                    for msg in item[1].messages
                )
            ),
            reverse=True,
        )

        for filename, old_proto_file_info in old_proto_files_infos_sorted_complexity:

            old_msg_sorted_complexity = sorted(
                enumerate(old_proto_file_info.messages),
                key=lambda elem: get_complexity_struct(
                    self.old_proto_files_infos, elem[1]
                ),
                reverse=True,
            )

            old_most_complex_msg_index, old_most_complex_msg = (
                old_msg_sorted_complexity[0]
            )
            mapping_info_most_complex_msg = self.get_message_mapping(
                new_proto_files_infos, old_proto_file_info, old_most_complex_msg
            )

            mapping_info_by_name[
                self.get_full_name_msg(
                    old_proto_file_info.package, old_most_complex_msg.name
                )
            ] = mapping_info_most_complex_msg

            for old_msg_index, old_msg in old_msg_sorted_complexity:
                if old_msg_index == old_most_complex_msg_index:
                    continue

                # index for new protos to start searching
                new_index_start_search = (
                    mapping_info_most_complex_msg.messages_name_with_index[0][1]
                    + (old_msg_index - old_most_complex_msg_index)
                )

                sliced_by_index_new_proto_files = {
                    key: value
                    for key, value in list(new_proto_files_infos.items())[
                        new_index_start_search:
                    ]
                }
                mapping_info_by_name[
                    self.get_full_name_msg(old_proto_file_info.package, old_msg.name)
                ] = self.get_message_mapping(
                    sliced_by_index_new_proto_files, old_proto_file_info, old_msg
                )

        return mapping_info_by_name

    def get_message_mapping(
        self,
        new_proto_files_infos: dict[str, ProtoFileInfo],
        old_proto_file_info: ProtoFileInfo,
        old_message: Message,
    ) -> MappingInfo:
        mapping_by_sim: dict[tuple[str, int], float] = {}
        is_found: bool = False

        for new_file_index, new_proto_file_info in enumerate(
            new_proto_files_infos.values()
        ):
            if is_found:
                break
            for new_message in new_proto_file_info.messages:
                old_comparator_info = MessageContextInfo(
                    file_info=old_proto_file_info,
                    message=old_message,
                    parent_context=None,
                )
                new_comparator_info = MessageContextInfo(
                    file_info=new_proto_file_info,
                    message=new_message,
                    parent_context=None,
                )

                if new_proto_file_info.package:
                    msg_full_name = (
                        new_proto_file_info.package.name + "." + new_message.name
                    )
                else:
                    msg_full_name = new_message.name

                similarity = self.compare_message(
                    old_comparator_info, new_comparator_info
                )
                mapping_by_sim[(msg_full_name, new_file_index)] = similarity
                if similarity == 1:
                    new_proto_files_infos[new_proto_file_info.filename].messages.remove(
                        new_message
                    )
                    is_found = True
                    break

        most_sim = max(mapping_by_sim.values(), default=0.0)
        messages_name_with_index = [
            key for key, value in mapping_by_sim.items() if value == most_sim
        ]
        return MappingInfo(messages_name_with_index, similarity=most_sim)

    def compare_message(
        self,
        old_comparator_info: MessageContextInfo,
        new_comparator_info: MessageContextInfo,
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
        old_comparator_context: MessageContextInfo,
        old_msg_element: MessageElement,
        new_comparator_context: MessageContextInfo,
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
        old_comparator_context: MessageContextInfo,
        old_one_of: OneOf,
        new_comparator_context: MessageContextInfo,
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
        old_comparator_context: MessageContextInfo,
        old_one_of_element: OneOfElement,
        new_comparator_context: MessageContextInfo,
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
        old_comparator_context: MessageContextInfo,
        old_field: Field,
        new_comparator_context: MessageContextInfo,
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
                old_comparator_context,
                old_field.type,
            )
            if related_old_struct_info is None:
                raise ValueError(f"Did not found struct {old_field.type}")

            related_old_file_info, related_old_struct = related_old_struct_info

            related_new_struct_info = get_related_struct(
                self.new_proto_files_infos,
                new_comparator_context,
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
                    MessageContextInfo(
                        file_info=related_old_file_info,
                        message=related_old_struct,
                        parent_context=old_comparator_context,
                    ),
                    MessageContextInfo(
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
