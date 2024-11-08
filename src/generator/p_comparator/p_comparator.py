from dataclasses import dataclass, field

from proto_schema_parser.ast import MapField

from src.generator.p_comparator.consts import PROTO_BASE_FIELDS
from src.generator.p_comparator.exceptions import TypeNotFound
from src.generator.p_comparator.models.p_enum import PEnum
from src.generator.p_comparator.models.p_file import PFile
from src.generator.p_comparator.models.p_folder import PFolder
from src.generator.p_comparator.models.p_message import PMessage, PField, POneOf


@dataclass
class PComparator:
    new_p_folder: PFolder
    old_p_folder: PFolder
    treated_new_msg_name: set[str] = field(init=False, default_factory=set)

    def get_mapping(self) -> dict[str, str]:
        mapping: dict[str, str] = {}

        # here we sort proto file by most complex msg because order INSIDE old file info is kept
        old_p_infos: list[tuple[PFile, list[tuple[int, PMessage]]]] = []
        for old_p_file in self.old_p_folder.files_by_filename.values():
            messages_info: list[tuple[int, PMessage]] = []
            for index, old_msg in enumerate(old_p_file.messages):
                messages_info.append((index, old_msg))
            messages_info.sort(
                key=lambda elem: self.old_p_folder.get_complexity_message(
                    old_p_file, elem[1], []
                ),
                reverse=True,
            )
            old_p_infos.append((old_p_file, messages_info))

        # sort by most complex so we can progressively eliminate
        old_p_infos.sort(
            key=lambda elem: self.old_p_folder.get_complexity_message(
                elem[0], elem[1][0][1], []
            ),
            reverse=True,
        )

        for old_p_file, messages_with_indexes in old_p_infos:
            # get most complex msg mapping for this old proto file info
            most_complex_match_index: tuple[int, int] | None = None
            for _old_index, _old_msg in messages_with_indexes:
                matching_new_msg = self.get_matching_for_old_msg(
                    old_p_file, _old_msg, 0
                )
                if matching_new_msg is not None:
                    most_complex_match_index = (
                        _old_index,
                        matching_new_msg[1],
                    )
                    mapping[matching_new_msg[0]] = (
                        f"{old_p_file.package}.{_old_msg.name}"
                    )
                    break

            if most_complex_match_index is None:
                continue

            old_most_complex_index, new_most_complex_related_index = (
                most_complex_match_index
            )
            for old_msg_index, old_msg in messages_with_indexes:
                if old_msg_index == old_most_complex_index:
                    continue

                # index for new protos to start searching
                new_index_start_search = new_most_complex_related_index + (
                    old_msg_index - old_most_complex_index
                )

                new_msg_mapping = self.get_matching_for_old_msg(
                    old_p_file, old_msg, new_index_start_search
                )
                if new_msg_mapping is None:
                    raise ValueError(f"Did not found mapping for {old_msg.name}")

                if new_msg_mapping[2] != 1:
                    print(f"{old_msg.name} : {new_msg_mapping}")

                mapping[new_msg_mapping[0]] = f"{old_p_file.package}.{old_msg.name}"

        return mapping

    def get_matching_for_old_msg(
        self,
        old_p_file: PFile,
        old_msg: PMessage,
        new_index: int,
    ) -> tuple[str, int, float] | None:

        mapping: tuple[str, int, float] | None = None

        # we just need new file index because 1 file = 1 enum or 1 message in new protos
        new_file_indexes = sorted(
            range(len(self.new_p_folder.files_by_filename.values())),
            key=lambda index: abs(index - new_index),
            reverse=True,
        )
        is_found: bool = False
        while not is_found:
            if len(new_file_indexes) == 0:
                break

            new_file_index = new_file_indexes.pop()
            new_p_file = list(self.new_p_folder.files_by_filename.values())[
                new_file_index
            ]
            for new_p_msg in new_p_file.messages:
                if new_p_msg.name in self.treated_new_msg_name:
                    continue
                similarity = self.compare_message(
                    old_p_file, old_msg, [], new_p_file, new_p_msg, []
                )
                if mapping is None or mapping[2] < similarity:
                    mapping = (new_p_msg.name, new_file_index, similarity)
                    if similarity == 1:
                        is_found = True
                        break

        return mapping if mapping and mapping[2] > 0.85 else None

    def compare_message(
        self,
        old_p_file: PFile,
        old_msg: PMessage,
        old_msg_stack: list[str],
        new_p_file: PFile,
        new_msg: PMessage,
        new_msg_stack: list[str],
    ) -> float:

        old_msg_stack.append(old_msg.name)
        new_msg_stack.append(new_msg.name)

        if len(old_msg.elements) == 0:
            return 1

        similarity: float = 0
        total_complexity: float = 0

        for index in range(len(old_msg.elements)):
            old_msg_elem = old_msg.elements[index]

            if type(old_msg_elem) is PField:
                complexity_msg_elem = self.old_p_folder.get_complexity_p_field(
                    old_p_file, old_msg, old_msg_elem, []
                )
            elif type(old_msg_elem) is POneOf:
                complexity_msg_elem = sum(
                    self.old_p_folder.get_complexity_p_field(
                        old_p_file, old_msg, one_of_elem, []
                    )
                    for one_of_elem in old_msg_elem.elements
                )
            elif type(old_msg_elem) is MapField:
                complexity_msg_elem = self.old_p_folder.get_complexity_map_field(
                    old_p_file, old_msg, old_msg_elem, []
                )
            else:
                continue

            total_complexity += complexity_msg_elem

            if len(new_msg.elements) - 1 < index:
                continue

            new_msg_elem = new_msg.elements[index]

            if type(old_msg_elem) is PField and type(new_msg_elem) is PField:
                similarity += (
                    self.compare_p_field(
                        old_p_file,
                        old_msg,
                        old_msg_elem,
                        old_msg_stack,
                        new_p_file,
                        new_msg,
                        new_msg_elem,
                        new_msg_stack,
                    )
                    * complexity_msg_elem
                )
            elif type(old_msg_elem) is POneOf and type(new_msg_elem) is POneOf:
                similarity += (
                    self.compare_p_one_of(
                        old_p_file,
                        old_msg,
                        old_msg_elem,
                        old_msg_stack,
                        new_p_file,
                        new_msg,
                        new_msg_elem,
                        new_msg_stack,
                    )
                    * complexity_msg_elem
                )
            elif type(old_msg_elem) is MapField and type(new_msg_elem) is MapField:
                similarity += (
                    self.compare_map_fields(
                        old_p_file,
                        old_msg,
                        old_msg_elem,
                        old_msg_stack,
                        new_p_file,
                        new_msg,
                        new_msg_elem,
                        new_msg_stack,
                    )
                    * complexity_msg_elem
                )

        return similarity / total_complexity

    def compare_p_one_of(
        self,
        old_p_file: PFile,
        old_p_msg: PMessage,
        old_p_one_of: POneOf,
        old_p_msg_stack: list[str],
        new_p_file: PFile,
        new_p_msg: PMessage,
        new_p_one_of: POneOf,
        new_p_msg_stack: list[str],
    ) -> float:
        total_complexity: float = 0
        similarity: float = 0
        for index in range(len(old_p_one_of.elements)):
            old_p_field = old_p_one_of.elements[index]

            complexity_msg_elem = self.old_p_folder.get_complexity_p_field(
                old_p_file, old_p_msg, old_p_field, []
            )

            total_complexity += complexity_msg_elem

            if len(new_p_one_of.elements) - 1 < index:
                continue

            new_p_field = new_p_one_of.elements[index]

            similarity += (
                self.compare_p_field(
                    old_p_file,
                    old_p_msg,
                    old_p_field,
                    old_p_msg_stack,
                    new_p_file,
                    new_p_msg,
                    new_p_field,
                    new_p_msg_stack,
                )
                * complexity_msg_elem
            )

        return similarity / total_complexity

    def compare_map_fields(
        self,
        old_p_file: PFile,
        old_p_msg: PMessage,
        old_map_field: MapField,
        old_p_msg_stack: list[str],
        new_p_file: PFile,
        new_p_msg: PMessage,
        new_map_field: MapField,
        new_p_msg_stack: list[str],
    ) -> float:

        similarity: float = 1
        coeff_check_failed: float = 1

        if old_map_field.key_type != new_map_field.key_type:
            coeff_check_failed += 1

        related_old_p_field = PField(
            type_name=old_map_field.value_type,
            name=old_map_field.name,
            cardinality=None,
            number=old_map_field.number,
        )
        related_new_p_field = PField(
            type_name=new_map_field.value_type,
            name=new_map_field.name,
            cardinality=None,
            number=new_map_field.number,
        )
        value_complexity = self.old_p_folder.get_complexity_map_field(
            old_p_file, old_p_msg, old_map_field, old_p_msg_stack
        )
        coeff_check_failed += (
            1
            - self.compare_p_field(
                old_p_file,
                old_p_msg,
                related_old_p_field,
                old_p_msg_stack,
                new_p_file,
                new_p_msg,
                related_new_p_field,
                new_p_msg_stack,
            )
        ) * value_complexity

        return similarity / coeff_check_failed

    def compare_p_field(
        self,
        old_p_file: PFile,
        old_p_msg: PMessage,
        old_p_field: PField,
        old_p_msg_stack: list[str],
        new_p_file: PFile,
        new_p_msg: PMessage,
        new_p_field: PField,
        new_p_msg_stack: list[str],
    ) -> float:

        similarity_score: float = 1
        coeff_check_failed: float = 1

        if old_p_field.number != new_p_field.number:
            coeff_check_failed += 1

        cleaned_old_type = (
            old_p_field.type_name[1:]
            if old_p_field.type_name.startswith(".")
            else old_p_field.type_name
        )

        if cleaned_old_type not in PROTO_BASE_FIELDS:
            if new_p_field.type_name in PROTO_BASE_FIELDS:
                return 0

            related_old_struct_with_file = (
                self.old_p_folder.get_msg_or_enum_from_type_name(
                    old_p_file, old_p_msg, old_p_field.type_name
                )
            )
            if related_old_struct_with_file:
                related_new_struct_with_file = (
                    self.new_p_folder.get_msg_or_enum_from_type_name(
                        new_p_file, new_p_msg, new_p_field.type_name
                    )
                )
                if not related_new_struct_with_file:
                    raise TypeNotFound(new_p_field.type_name)

                related_old_file, related_old_struct = related_old_struct_with_file
                related_new_file, related_new_struct = related_new_struct_with_file

                if (
                    type(related_old_struct) is PMessage
                    and type(related_new_struct) is PMessage
                ):
                    if related_old_struct.name in old_p_msg_stack:
                        if related_new_struct.name not in new_p_msg_stack:
                            return 0
                        return 1
                    return self.compare_message(
                        related_old_file,
                        related_old_struct,
                        old_p_msg_stack,
                        related_new_file,
                        related_new_struct,
                        new_p_msg_stack,
                    )
                elif (
                    type(related_old_struct) is PEnum
                    and type(related_new_struct) is PEnum
                ):
                    return self.compare_enum(related_old_struct, related_new_struct)
                else:
                    return 0

        elif cleaned_old_type != new_p_field.type_name:
            coeff_check_failed += 2

        if old_p_field.cardinality != new_p_field.cardinality:
            coeff_check_failed += 1

        return similarity_score / coeff_check_failed

    def compare_enum(self, old_enum: PEnum, new_enum: PEnum) -> float:
        old_enum_names = [element.name for element in old_enum.elements]
        new_enum_names = [element.name for element in new_enum.elements]
        return len(set(old_enum_names) & set(new_enum_names)) / len(old_enum_names)
