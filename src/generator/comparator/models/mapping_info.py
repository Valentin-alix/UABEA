from dataclasses import dataclass

from src.generator.comparator.custom_types import Percentage


@dataclass
class MappingInfo:
    messages_name: list[str]
    similarity: Percentage
