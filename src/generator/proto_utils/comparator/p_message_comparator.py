from dataclasses import dataclass

from proto_schema_parser import FieldCardinality

from src.generator.proto_utils.comparator.p_enum_comparator import PEnumComparator
from src.generator.proto_utils.consts import PROTO_BASE_FIELDS
from src.generator.proto_utils.exceptions import TypeNotFound
from src.generator.proto_utils.models.p_enum import PEnum
from src.generator.proto_utils.models.p_file import PFile
from src.generator.proto_utils.models.p_folder import PFolder
from src.generator.proto_utils.models.p_message import (
    PMessage,
    PField,
    POneOf,
    PMapField,
)


@dataclass
class ContextMessage:
    p_folder: PFolder
    p_file: PFile
    p_msg: PMessage
    p_stack_p_msg_id: set[int]


class PMessageComparator:
    @staticmethod
    def compare_message(
        old_context_msg: ContextMessage, new_context_msg: ContextMessage
    ) -> float:

        old_context_msg.p_stack_p_msg_id.add(id(old_context_msg.p_msg))
        new_context_msg.p_stack_p_msg_id.add(id(new_context_msg.p_msg))

        if len(old_context_msg.p_msg.elements) == 0:
            if len(new_context_msg.p_msg.elements) == 0:
                return 1
            return 0

        similarity: float = 0
        total_complexity: float = 0

        if len(old_context_msg.p_msg.elements) >= len(new_context_msg.p_msg.elements):
            first_context_msg = old_context_msg
            second_context_msg = new_context_msg
        else:
            first_context_msg = new_context_msg
            second_context_msg = old_context_msg

        for index in range(len(first_context_msg.p_msg.elements)):
            first_msg_elem = first_context_msg.p_msg.elements[index]
            if type(first_msg_elem) is PField:
                first_complexity_msg_elem = (
                    first_context_msg.p_folder.get_reliability_p_field(
                        first_context_msg.p_file,
                        first_context_msg.p_msg,
                        first_msg_elem,
                        set(),
                    )
                )
            elif type(first_msg_elem) is POneOf:
                first_complexity_msg_elem = sum(
                    first_context_msg.p_folder.get_reliability_p_field(
                        first_context_msg.p_file,
                        first_context_msg.p_msg,
                        one_of_elem,
                        set(),
                    )
                    for one_of_elem in first_msg_elem.elements
                )
            elif type(first_msg_elem) is PMapField:
                first_complexity_msg_elem = (
                    first_context_msg.p_folder.get_reliability_map_field(
                        first_context_msg.p_file,
                        first_context_msg.p_msg,
                        first_msg_elem,
                        set(),
                    )
                )
            else:
                continue

            total_complexity += first_complexity_msg_elem

            if len(second_context_msg.p_msg.elements) - 1 < index:
                continue

            second_msg_elem = second_context_msg.p_msg.elements[index]

            if type(first_msg_elem) is PField and type(second_msg_elem) is PField:
                similarity += (
                    PMessageComparator.compare_p_field(
                        first_context_msg,
                        first_msg_elem,
                        second_context_msg,
                        second_msg_elem,
                    )
                    * first_complexity_msg_elem
                )
            elif type(first_msg_elem) is POneOf and type(second_msg_elem) is POneOf:
                similarity += (
                    PMessageComparator.compare_p_one_of(
                        first_context_msg,
                        first_msg_elem,
                        second_context_msg,
                        second_msg_elem,
                    )
                    * first_complexity_msg_elem
                )
            elif (
                type(first_msg_elem) is PMapField and type(second_msg_elem) is PMapField
            ):
                similarity += (
                    PMessageComparator.compare_map_fields(
                        first_context_msg,
                        first_msg_elem,
                        second_context_msg,
                        second_msg_elem,
                    )
                    * first_complexity_msg_elem
                )

        return similarity / total_complexity

    @staticmethod
    def compare_p_one_of(
        old_context_msg: ContextMessage,
        old_p_one_of: POneOf,
        new_context_msg: ContextMessage,
        new_p_one_of: POneOf,
    ) -> float:
        total_complexity: float = 0
        similarity: float = 0
        for index in range(len(old_p_one_of.elements)):
            old_p_field = old_p_one_of.elements[index]

            complexity_msg_elem = old_context_msg.p_folder.get_reliability_p_field(
                old_context_msg.p_file, old_context_msg.p_msg, old_p_field, set()
            )

            total_complexity += complexity_msg_elem

            if len(new_p_one_of.elements) - 1 < index:
                continue

            new_p_field = new_p_one_of.elements[index]

            similarity += (
                PMessageComparator.compare_p_field(
                    old_context_msg, old_p_field, new_context_msg, new_p_field
                )
                * complexity_msg_elem
            )

        return similarity / total_complexity

    @staticmethod
    def compare_map_fields(
        old_context: ContextMessage,
        old_p_map_field: PMapField,
        new_context_msg: ContextMessage,
        new_p_map_field: PMapField,
    ) -> float:

        similarity: float = 1
        coeff_check_failed: float = 1

        if old_p_map_field.key_type != new_p_map_field.key_type:
            coeff_check_failed += 1

        value_complexity = old_context.p_folder.get_reliability_map_field(
            old_context.p_file,
            old_context.p_msg,
            old_p_map_field,
            old_context.p_stack_p_msg_id,
        )
        coeff_check_failed += (
            1
            - PMessageComparator.compare_p_field(
                old_context,
                old_p_map_field.value_p_field,
                new_context_msg,
                new_p_map_field.value_p_field,
            )
        ) * value_complexity

        return similarity / coeff_check_failed

    @staticmethod
    def compare_p_field(
        old_context: ContextMessage,
        old_p_field: PField,
        new_context: ContextMessage,
        new_p_field: PField,
    ) -> float:
        similarity_score: float = 0

        if (old_p_field.cardinality is FieldCardinality.REPEATED) == (
            new_p_field.cardinality is FieldCardinality.REPEATED
        ):
            similarity_score += 0.5

        if old_p_field.type_name in PROTO_BASE_FIELDS:
            if old_p_field.type_name != new_p_field.type_name:
                return 0
            similarity_score += 2
            return similarity_score / 2.5

        if new_p_field.type_name in PROTO_BASE_FIELDS:
            return 0

        related_old_struct_with_file = (
            old_context.p_folder.get_msg_or_enum_from_type_name(
                old_context.p_file, old_context.p_msg, old_p_field.type_name
            )
        )
        if not related_old_struct_with_file:
            raise TypeNotFound(old_p_field.type_name)

        related_new_struct_with_file = (
            new_context.p_folder.get_msg_or_enum_from_type_name(
                new_context.p_file, new_context.p_msg, new_p_field.type_name
            )
        )
        if not related_new_struct_with_file:
            raise TypeNotFound(new_p_field.type_name)

        related_old_file, related_old_struct = related_old_struct_with_file
        related_new_file, related_new_struct = related_new_struct_with_file

        if isinstance(related_old_struct, PMessage) and isinstance(
            related_new_struct, PMessage
        ):
            if id(related_old_struct) in old_context.p_stack_p_msg_id:
                if id(related_new_struct) not in new_context.p_stack_p_msg_id:
                    return 0
                # found msg in stack, we can assume they are equal to avoid recursion error
                return 1

            reliability_related_old_msg = old_context.p_folder.get_reliability_message(
                related_old_file, related_old_struct, set()
            )
            related_old_context_msg = ContextMessage(
                p_folder=old_context.p_folder,
                p_file=related_old_file,
                p_msg=related_old_struct,
                p_stack_p_msg_id=old_context.p_stack_p_msg_id,
            )
            related_new_context_msg = ContextMessage(
                p_folder=new_context.p_folder,
                p_file=related_new_file,
                p_msg=related_new_struct,
                p_stack_p_msg_id=new_context.p_stack_p_msg_id,
            )
            return (
                (
                    PMessageComparator.compare_message(
                        related_old_context_msg, related_new_context_msg
                    )
                    * (reliability_related_old_msg + similarity_score)
                )
            ) / (reliability_related_old_msg + 0.5)
        elif type(related_old_struct) is PEnum and type(related_new_struct) is PEnum:

            return (
                PEnumComparator.compare_enum(related_old_struct, related_new_struct)
                * related_old_struct.reliability
                + similarity_score
            ) / (related_old_struct.reliability + 0.5)

        return 0
