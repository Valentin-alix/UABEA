from dataclasses import dataclass, field

import icecream
from proto_schema_parser.ast import (
    Field,
    OneOf,
    OneOfElement,
    Enum,
    EnumElement,
    EnumValue,
)

from src.generator.comparator.consts import PROTO_BASE_FIELDS
from src.generator.comparator.custom_types import Percentage
from src.generator.comparator.models.mapping_info import MappingInfo
from src.generator.comparator.models.message_context_info import (
    MessageContextInfo,
)
from src.generator.comparator.models.proto_file_info import ProtoFileInfo
from src.generator.comparator.utils import get_sort_value_msg_element, get_full_name_msg


@dataclass
class ProtoComparator:
    new_proto_files_infos: dict[str, ProtoFileInfo]
    old_proto_files_infos: dict[str, ProtoFileInfo]
    new_filenames_found: list[str] = field(init=False, default_factory=list)

    def get_all_messages_mapping(self) -> dict[str, MappingInfo]:
        self.new_filenames_found.clear()
        mapping_info_by_name: dict[str, MappingInfo] = {}

        # here we sort proto file by most complex msg
        old_proto_files_infos_sorted_complexity = sorted(
            self.old_proto_files_infos.items(),
            key=lambda filename_with_file_info: max(
                (
                    MessageContextInfo(
                        message=msg,
                        file_info=filename_with_file_info[1],
                        parent_context=None,
                        file_info_by_name=self.old_proto_files_infos,
                    ).get_complexity()
                    for msg in filename_with_file_info[1].messages
                )
            ),
            reverse=True,
        )

        for filename, old_proto_file_info in old_proto_files_infos_sorted_complexity:
            _old_complex_index_found: int | None = None
            _new_related_index_found: int | None = None

            for _old_index, _old_msg in sorted(
                enumerate(old_proto_file_info.messages),
                key=lambda index_with_msg: MessageContextInfo(
                    message=index_with_msg[1],
                    file_info=old_proto_file_info,
                    parent_context=None,
                    file_info_by_name=self.old_proto_files_infos,
                ).get_complexity(),
                reverse=True,
            ):
                _old_msg_info = MessageContextInfo(
                    file_info_by_name=self.old_proto_files_infos,
                    parent_context=None,
                    file_info=old_proto_file_info,
                    message=_old_msg,
                )
                _old_mapping_info_msg = self.get_message_mapping(_old_msg_info, 0)
                if _old_mapping_info_msg is not None:
                    _old_complex_index_found = _old_index
                    _new_related_index_found = _old_mapping_info_msg.name_with_index[0]
                    mapping_info_by_name[
                        get_full_name_msg(old_proto_file_info.package, _old_msg.name)
                    ] = _old_mapping_info_msg
                    break

            if _old_complex_index_found is None or _new_related_index_found is None:
                continue

            for old_msg_index, old_msg in enumerate(old_proto_file_info.messages):
                if old_msg_index == _old_complex_index_found:
                    continue

                old_msg_info = MessageContextInfo(
                    file_info_by_name=self.old_proto_files_infos,
                    parent_context=None,
                    file_info=old_proto_file_info,
                    message=old_msg,
                )

                # index for new protos to start searching
                new_index_start_search = _new_related_index_found + (
                    old_msg_index - _old_complex_index_found
                )

                new_msg_mapping = self.get_message_mapping(
                    old_msg_info, new_index_start_search
                )
                if new_msg_mapping is None:
                    raise ValueError(
                        f"Did not found mapping for {old_msg_info.message.name}"
                    )
                mapping_info_by_name[
                    get_full_name_msg(old_proto_file_info.package, old_msg.name)
                ] = new_msg_mapping

        count_new_proto_not_found = len(
            set(self.new_proto_files_infos.keys() ^ self.new_filenames_found)
        )
        icecream.ic(
            f"ratio not found : {count_new_proto_not_found / len(self.new_filenames_found)}"
        )

        return mapping_info_by_name

    def get_message_mapping(
        self,
        old_msg_info: MessageContextInfo,
        new_index_start_search: int,
    ) -> MappingInfo | None:
        mapping_info: MappingInfo | None = None

        open_proto_files_index = sorted(
            range(len(self.new_proto_files_infos.values())),
            key=lambda index: abs(index - new_index_start_search),
            reverse=True,
        )

        is_found: bool = False
        while not is_found:
            if len(open_proto_files_index) == 0:
                break
            # we just need new file index because 1 file = 1 enum or 1 message in new protos
            new_file_index = open_proto_files_index.pop()
            new_proto_file_info = list(self.new_proto_files_infos.values())[
                new_file_index
            ]
            for new_msg in new_proto_file_info.messages:
                new_msg_info = MessageContextInfo(
                    file_info_by_name=self.new_proto_files_infos,
                    file_info=new_proto_file_info,
                    message=new_msg,
                    parent_context=None,
                )
                similarity = self.compare_message(old_msg_info, new_msg_info)
                if mapping_info is None or mapping_info.similarity < similarity:
                    new_msg_full_name = get_full_name_msg(
                        new_proto_file_info.package, new_msg.name
                    )
                    mapping_info = MappingInfo(
                        name_with_index=(new_file_index, new_msg_full_name),
                        similarity=similarity,
                    )
                    if (
                        similarity == 1
                        and new_proto_file_info.filename not in self.new_filenames_found
                    ):
                        self.new_filenames_found.append(new_proto_file_info.filename)
                        is_found = True
                        break

        return mapping_info if mapping_info and mapping_info.similarity > 0.75 else None

    def compare_message(
        self,
        old_msg_info: MessageContextInfo,
        new_msg_info: MessageContextInfo,
    ) -> Percentage:

        old_msg_fields: list[Field | OneOf] = [
            elem
            for elem in old_msg_info.message.elements
            if type(elem) is Field or type(elem) is OneOf
        ]
        new_msg_fields: list[Field | OneOf] = [
            elem
            for elem in new_msg_info.message.elements
            if type(elem) is Field or type(elem) is OneOf
        ]
        if len(old_msg_fields) != len(new_msg_fields):
            return 0

        if len(old_msg_fields) == 0:
            return 1

        old_msg_fields.sort(key=get_sort_value_msg_element)
        new_msg_fields.sort(key=get_sort_value_msg_element)

        elements_similarity_score: float = 0
        for index in range(len(old_msg_fields)):
            elements_similarity_score += self.compare_msg_elements(
                old_msg_info, old_msg_fields[index], new_msg_info, new_msg_fields[index]
            )

        return Percentage(elements_similarity_score / len(old_msg_fields))

    def compare_msg_elements(
        self,
        old_msg_context: MessageContextInfo,
        old_msg_element: OneOf | Field,
        new_msg_context: MessageContextInfo,
        new_msg_element: OneOf | Field,
    ) -> Percentage:
        if type(old_msg_element) is not type(new_msg_element):
            return 0

        if type(old_msg_element) is OneOf and type(new_msg_element) is OneOf:
            return self.compare_one_ofs(
                old_msg_context,
                old_msg_element,
                new_msg_context,
                new_msg_element,
            )

        if type(old_msg_element) is Field and type(new_msg_element) is Field:
            return self.compare_fields(
                old_msg_context,
                old_msg_element,
                new_msg_context,
                new_msg_element,
            )

        return 1

    def compare_one_ofs(
        self,
        old_msg_context: MessageContextInfo,
        old_one_of: OneOf,
        new_msg_context: MessageContextInfo,
        new_one_of: OneOf,
    ) -> Percentage:
        if len(old_one_of.elements) != len(new_one_of.elements):
            return 0

        if len(old_one_of.elements) == 0:
            return 1

        elements_similarity_score: float = 0
        for index in range(len(old_one_of.elements)):
            elements_similarity_score += self.compare_one_of_element(
                old_msg_context,
                old_one_of.elements[index],
                new_msg_context,
                new_one_of.elements[index],
            )

        return Percentage(elements_similarity_score / len(old_one_of.elements))

    def compare_one_of_element(
        self,
        old_msg_context: MessageContextInfo,
        old_one_of_element: OneOfElement,
        new_msg_context: MessageContextInfo,
        new_one_of_element: OneOfElement,
    ) -> Percentage:
        if type(old_one_of_element) is not type(new_one_of_element):
            return 0

        if type(old_one_of_element) is Field and type(new_one_of_element) is Field:
            return self.compare_fields(
                old_msg_context,
                old_one_of_element,
                new_msg_context,
                new_one_of_element,
            )

        return 1

    def compare_fields(
        self,
        old_msg_context: MessageContextInfo,
        old_field: Field,
        new_msg_context: MessageContextInfo,
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

            related_old_struct_info = (
                old_msg_context.get_msg_info_or_enum_from_type_name(old_field.type)
            )
            if related_old_struct_info is None:
                raise ValueError(f"Did not found struct {old_field.type}")

            related_new_struct_info = (
                new_msg_context.get_msg_info_or_enum_from_type_name(
                    new_field.type,
                )
            )
            if related_new_struct_info is None:
                raise ValueError(
                    f"Did not found struct {new_field.type} at file info {new_msg_context.message.name}"
                )
            if (
                type(related_old_struct_info) is MessageContextInfo
                and type(related_new_struct_info) is MessageContextInfo
            ):
                old_depth = old_msg_context.get_depth_in_parent(
                    related_old_struct_info.message.name
                )
                # to avoid infinite recursion
                if old_depth is not None:
                    new_depth = new_msg_context.get_depth_in_parent(
                        related_new_struct_info.message.name
                    )
                    if new_depth == old_depth:
                        return 1
                    return 0

                return self.compare_message(
                    related_old_struct_info, related_new_struct_info
                )

            if (
                type(related_old_struct_info) is Enum
                and type(related_new_struct_info) is Enum
            ):
                return self.compare_enum(
                    related_old_struct_info, related_new_struct_info
                )

            return 0

        elif cleaned_old_type != new_field.type:
            coeff_check_failed += 2

        if old_field.cardinality != new_field.cardinality:
            coeff_check_failed += 1

        return Percentage(similarity_score / coeff_check_failed)

    @staticmethod
    def compare_enum(old_enum: Enum, new_enum: Enum) -> Percentage:
        old_enum_names = [
            element.name for element in old_enum.elements if type(element) is EnumValue
        ]
        new_enum_names = [
            element.name for element in new_enum.elements if type(element) is EnumValue
        ]
        return Percentage(
            len(set(old_enum_names) & set(new_enum_names)) / len(old_enum_names)
        )

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
