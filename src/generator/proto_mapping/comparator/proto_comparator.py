from dataclasses import dataclass

from proto_schema_parser import Message
from proto_schema_parser.ast import Enum

from src.generator.proto_mapping.comparator.proto_message_comparator import (
    ProtoMessageInfo,
    ProtoMessageComparator,
)


@dataclass
class ProtoInfo:
    message_by_name: dict[str, Message]
    enum_by_name: dict[str, Enum]


@dataclass
class ProtoComparator:
    old_proto_info: ProtoInfo
    new_proto_info: ProtoInfo

    def get_most_probable_message_mapping(self) -> dict[str, str]:
        mapping = self.get_messages_mapping()
        sorted_mapping = sorted(
            mapping.items(), key=lambda elem: elem[1][1], reverse=True
        )

        most_probable_matching: dict[str, str] = {}
        for new_msg_name, (probable_old_msg_names, _) in sorted_mapping:
            for old_msg_name in probable_old_msg_names:
                if old_msg_name in most_probable_matching.values():
                    continue
                most_probable_matching[new_msg_name] = old_msg_name
                break

        return most_probable_matching

    def get_messages_mapping(self) -> dict[str, tuple[list[str], float]]:
        mapping: dict[str, tuple[list[str], float]] = {}

        for new_msg in self.new_proto_info.message_by_name.values():
            mapping_by_sim: dict[str, float] = {}
            new_msg_info = ProtoMessageInfo(
                parent_message_info=None,
                message=new_msg,
                external_messages=self.new_proto_info.message_by_name,
                external_enums=self.new_proto_info.enum_by_name,
            )
            for old_msg in self.old_proto_info.message_by_name.values():
                if new_msg.name == "hcq" and old_msg.name == "TaxCollectorTopListEvent":
                    print()
                old_msg_info = ProtoMessageInfo(
                    parent_message_info=None,
                    message=old_msg,
                    external_messages=self.old_proto_info.message_by_name,
                    external_enums=self.old_proto_info.enum_by_name,
                )
                mapping_by_sim[old_msg.name] = ProtoMessageComparator(
                    message_info_1=new_msg_info, message_info_2=old_msg_info
                ).compare()

            most_sim = max(mapping_by_sim.values(), default=0.0)
            mapping[new_msg.name] = (
                [key for key, value in mapping_by_sim.items() if value == most_sim],
                most_sim,
            )

        return mapping
