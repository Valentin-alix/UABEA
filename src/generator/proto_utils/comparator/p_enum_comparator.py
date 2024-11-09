from src.generator.proto_utils.models.p_enum import PEnum


class PEnumComparator:
    @staticmethod
    def compare_enum(old_enum: PEnum, new_enum: PEnum) -> float:
        old_enum_names = {element.name for element in old_enum.elements}
        new_enum_names = {element.name for element in new_enum.elements}
        return 1 / (1 + len(old_enum_names.symmetric_difference(new_enum_names)))
