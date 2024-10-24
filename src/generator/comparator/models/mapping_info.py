from dataclasses import dataclass

from src.generator.comparator.custom_types import Percentage


@dataclass
class MappingInfo:
    messages_index_with_name: list[tuple[int, str]]
    similarity: Percentage
