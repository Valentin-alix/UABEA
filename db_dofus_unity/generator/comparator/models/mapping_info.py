from dataclasses import dataclass

from db_dofus_unity.generator.comparator.custom_types import Percentage


@dataclass
class MappingInfo:
    messages_name: list[str]
    similarity: Percentage
