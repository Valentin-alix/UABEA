from dataclasses import dataclass

from src.generator.comparator.custom_types import Percentage


@dataclass
class MappingInfo:
    name_with_index: tuple[int, str]
    similarity: Percentage
