from dataclasses import dataclass

from proto_schema_parser import Message
from proto_schema_parser.ast import Enum

from src.generator.comparator.proto_message_comparator import (
    ProtoMessageInfo,
    ProtoMessageComparator,
)


@dataclass
class MappingInfo:
    messages_name: list[str]
    similarity: float


@dataclass
class ProtoInfo:
    root_messages: list[Message]
    message_by_import_name: dict[str, Message]
    enum_by_import_name: dict[str, Enum]


@dataclass
class ProtoComparator:
    old_proto_info: ProtoInfo
    new_proto_info: ProtoInfo

    def get_most_probable_messages_mapping(self) -> dict[str, str]:
        mapping = self.get_messages_mapping()
        mapping_sorted_probable = sorted(
            mapping.items(), key=lambda elem: elem[1].similarity, reverse=True
        )
        most_probable_matching: dict[str, str] = {}
        for new_msg_name, mapping_info in mapping_sorted_probable:
            for old_msg_name in mapping_info.messages_name:
                if old_msg_name in most_probable_matching.values():
                    continue
                most_probable_matching[new_msg_name] = old_msg_name
                break

        return most_probable_matching

    def get_messages_mapping(self) -> dict[str, MappingInfo]:
        mapping_info_by_name: dict[str, MappingInfo] = {}

        for new_msg in self.new_proto_info.root_messages:
            mapping_info_by_name[new_msg.name] = self.get_message_mapping(new_msg)

        return mapping_info_by_name

    def get_message_mapping(self, new_msg: Message) -> MappingInfo:
        mapping_by_sim: dict[str, float] = {}

        new_msg_info = ProtoMessageInfo(
            parent_message_info=None,
            message=new_msg,
            external_messages=self.new_proto_info.message_by_import_name,
            external_enums=self.new_proto_info.enum_by_import_name,
        )
        for old_msg in self.old_proto_info.root_messages:
            if new_msg.name == "gxl" and old_msg.name == "ClientUIOpenedEvent":
                print()

            old_msg_info = ProtoMessageInfo(
                parent_message_info=None,
                message=old_msg,
                external_messages=self.old_proto_info.message_by_import_name,
                external_enums=self.old_proto_info.enum_by_import_name,
            )
            mapping_by_sim[old_msg.name] = ProtoMessageComparator(
                message_info_1=new_msg_info, message_info_2=old_msg_info
            ).compare()

        most_sim = max(mapping_by_sim.values(), default=0.0)
        messages_name = [
            key for key, value in mapping_by_sim.items() if value == most_sim
        ]

        return MappingInfo(messages_name, similarity=most_sim)
