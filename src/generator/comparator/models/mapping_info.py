from dataclasses import dataclass

from src.generator.comparator.custom_types import Percentage


@dataclass
class MappingInfo:
    messages_name_with_index: list[tuple[str, int]]
    similarity: Percentage
