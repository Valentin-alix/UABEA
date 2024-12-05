from dataclasses import dataclass, field
from typing import Iterable

from src.generator.proto_utils.comparator.p_message_comparator import (
    PMessageComparator,
    ContextMessage,
)
from src.generator.proto_utils.models.p_enum import PEnum, PEnumElement
from src.generator.proto_utils.models.p_file import PFile
from src.generator.proto_utils.models.p_folder import PFolder
from src.generator.proto_utils.models.p_message import PMessage


@dataclass
class PComparator:
    new_p_folder: PFolder
    old_p_folder: PFolder
    treated_new_msg_name: set[str] = field(init=False, default_factory=set)

    def get_mapping(self) -> dict[str, str]:
        mapping: dict[str, str] = {}
        uncompleted_mapping: dict[str, tuple[str, float]] = {}

        # here we sort proto file by most reliable msg because order INSIDE old file info is kept
        old_sorted_p_file_infos: list[
            tuple[PFile, list[tuple[int, PMessage, tuple[bool, float]]], bool, set[str]]
        ] = [
            (elem[0], elem[1], False, set())
            for elem in self.get_sorted_p_file_by_reliability(self.old_p_folder)
        ]

        while len(old_sorted_p_file_infos) > 0:
            (
                old_p_file,
                old_p_messages_with_indexes,
                is_last_chance,
                exclude_new_most_complex_name,
            ) = old_sorted_p_file_infos.pop(0)

            curr_mapping_old_file: dict[str, str] = {}
            curr_uncompleted_mapping: dict[str, tuple[str, float]] = {}
            curr_treated_new_msg_name: set[str] = self.treated_new_msg_name.copy()

            # get most reliable msg mapping for this old proto file info
            most_reliable_matched: tuple[int, int, str] | None
            for old_index, old_p_msg, _ in old_p_messages_with_indexes:
                matching_new_p_msg = self.get_matching_for_old_p_msg(
                    old_p_file,
                    old_p_msg,
                    curr_treated_new_msg_name | exclude_new_most_complex_name,
                    None,
                    1,
                )
                if matching_new_p_msg is not None:
                    most_reliable_matched = (
                        old_index,
                        matching_new_p_msg[1],
                        matching_new_p_msg[0],
                    )
                    curr_treated_new_msg_name.add(matching_new_p_msg[0])
                    curr_mapping_old_file[matching_new_p_msg[0]] = (
                        f"{old_p_file.package}.{old_p_msg.name}"
                    )
                    break
            else:
                if is_last_chance:
                    raise ValueError(f"{old_p_file.filename} could not be resolved")

                old_sorted_p_file_infos.append(
                    (
                        old_p_file,
                        old_p_messages_with_indexes,
                        True,
                        set(),
                    )
                )
                continue

            (
                old_most_reliable_index,
                new_most_reliable_related_index,
                new_most_reliable_msg_name,
            ) = most_reliable_matched

            for old_p_msg_index, old_p_msg, _ in old_p_messages_with_indexes:
                if old_p_msg_index == old_most_reliable_index:
                    continue

                # index for new protos to start searching
                new_index_start_search = new_most_reliable_related_index + (
                    old_p_msg_index - old_most_reliable_index
                )

                new_msg_mapping = self.get_matching_for_old_p_msg(
                    old_p_file,
                    old_p_msg,
                    curr_treated_new_msg_name,
                    new_index_start_search,
                )
                if new_msg_mapping is None:
                    if is_last_chance:
                        print(f"{old_p_msg.name} could not be resolved")
                        continue

                    # group is not coherent, put this group at last & exclude this most complex index
                    exclude_new_most_complex_name.add(new_most_reliable_msg_name)
                    old_sorted_p_file_infos.append(
                        (
                            old_p_file,
                            old_p_messages_with_indexes,
                            False,
                            exclude_new_most_complex_name,
                        )
                    )
                    break

                if new_msg_mapping[2] != 1:
                    curr_uncompleted_mapping[old_p_msg.name] = (
                        old_p_msg.name,
                        new_msg_mapping[2],
                    )

                curr_treated_new_msg_name.add(new_msg_mapping[0])
                curr_mapping_old_file[new_msg_mapping[0]] = (
                    f"{old_p_file.package}.{old_p_msg.name}"
                )
            else:
                self.treated_new_msg_name = curr_treated_new_msg_name
                mapping |= curr_mapping_old_file
                uncompleted_mapping |= curr_uncompleted_mapping

        for new_p_file in self.new_p_folder.files_by_filename.values():
            for new_msg in new_p_file.messages:
                if new_msg.name in self.treated_new_msg_name:
                    continue
                print(f"unknown new msg : {new_msg.name}")

        print(f"uncompleted : {uncompleted_mapping}")

        return mapping

    def get_sorted_p_file_by_reliability(
        self, p_folder: PFolder
    ) -> list[tuple[PFile, list[tuple[int, PMessage, tuple[bool, float]]]]]:
        p_infos: list[tuple[PFile, list[tuple[int, PMessage, tuple[bool, float]]]]] = []
        p_messages: list[PMessage] = [
            p_message
            for p_file in p_folder.files_by_filename.values()
            for p_message in p_file.messages
        ]

        for p_file in p_folder.files_by_filename.values():
            messages_infos: list[tuple[int, PMessage, tuple[bool, float]]] = []
            for index, p_msg in enumerate(p_file.messages):
                reliability_msg = (
                    not self.does_duplicate_msg_exist(p_msg, p_messages),
                    p_folder.get_reliability_message(p_file, p_msg, set()),
                )
                messages_infos.append((index, p_msg, reliability_msg))
            messages_infos.sort(key=lambda elem: elem[2], reverse=True)
            p_infos.append((p_file, messages_infos))

        # sort by most reliable so we can progressively eliminate
        p_infos.sort(
            key=lambda elem: elem[1][0][2],
            reverse=True,
        )
        return p_infos

    def does_duplicate_msg_exist(
        self, old_msg: PMessage, messages: Iterable[PMessage]
    ) -> bool:
        for msg in messages:
            if msg.name == old_msg.name:
                continue
            if msg.are_strict_equals(old_msg):
                return True
        return False

    def get_matching_for_old_p_msg(
        self,
        old_p_file: PFile,
        old_p_msg: PMessage,
        exclude_msg_name: set[str],
        new_index: int | None,
        limit: float = 0.85,
    ) -> tuple[str, int, float] | None:

        mapping: tuple[str, int, float] | None = None

        # we just need new file index because 1 file = 1 enum or 1 message in new protos
        if new_index:
            new_file_indexes = sorted(
                range(len(self.new_p_folder.p_file_array)),
                key=lambda index: abs(index - new_index),
            )
        else:
            new_file_indexes = list(range(len(self.new_p_folder.p_file_array)))

        is_found: bool = False
        while not is_found:
            if len(new_file_indexes) == 0:
                break

            new_file_index = new_file_indexes.pop(0)
            if new_index is not None and abs(new_file_index - new_index) > 12:
                return None

            new_p_file = self.new_p_folder.p_file_array[new_file_index]

            for new_p_msg in new_p_file.messages:
                if new_p_msg.name in exclude_msg_name:
                    continue
                old_context_msg = ContextMessage(
                    p_folder=self.old_p_folder,
                    p_stack_p_msg_id=set(),
                    p_msg=old_p_msg,
                    p_file=old_p_file,
                )
                new_context_msg = ContextMessage(
                    p_folder=self.new_p_folder,
                    p_stack_p_msg_id=set(),
                    p_msg=new_p_msg,
                    p_file=new_p_file,
                )

                similarity = PMessageComparator.compare_message(
                    old_context_msg, new_context_msg
                )
                if mapping is None or mapping[2] < similarity:
                    mapping = (new_p_msg.name, new_file_index, similarity)
                    if similarity >= limit:
                        is_found = True
                        break

        if mapping and mapping[2] >= limit:
            return mapping
        return None


if __name__ == "__main__":
    enum_1 = PEnum(
        name="yolo",
        elements=[
            PEnumElement(name="ONE", value=1),
            PEnumElement(name="TWO", value=2),
            PEnumElement(name="THREE", value=3),
            PEnumElement(name="FOUR", value=4),
        ],
    )
    enum_2 = PEnum(
        name="lala",
        elements=[
            PEnumElement(name="ONE", value=1),
            PEnumElement(name="TWO", value=2),
            PEnumElement(name="THREE", value=3),
            PEnumElement(name="FOUR", value=4),
            PEnumElement(name="FIVE", value=5),
        ],
    )
    old_enum_names = {element.name for element in enum_1.elements}
    new_enum_names = {element.name for element in enum_2.elements}
    temp = len(old_enum_names.symmetric_difference(new_enum_names))
    print(temp)
