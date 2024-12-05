from src.generator.proto_utils.models.p_enum import PEnum, PEnumElement


class PEnumComparator:
    @staticmethod
    def compare_enum(old_enum: PEnum, new_enum: PEnum) -> float:
        old_enum_names = {element.name for element in old_enum.elements}
        new_enum_names = {element.name for element in new_enum.elements}
        return 1 / (
            1
            + (
                len(old_enum_names.symmetric_difference(new_enum_names))
                / len(old_enum_names)
            )
        )


if __name__ == "__main__":
    enum1 = PEnum(
        name="t",
        elements=[
            PEnumElement(name="SOCIAL_GROUP_OPERATION_OK", value=0),
            PEnumElement(name="SOCIAL_GROUP_ERROR_NAME_INVALID", value=1),
            PEnumElement(name="SOCIAL_GROUP_ERROR_ALREADY_IN_GROUP", value=2),
            PEnumElement(name="SOCIAL_GROUP_ERROR_NAME_ALREADY_EXISTS", value=3),
            PEnumElement(name="SOCIAL_GROUP_ERROR_LEAVE", value=4),
            PEnumElement(name="SOCIAL_GROUP_ERROR_CANCEL", value=5),
            PEnumElement(name="SOCIAL_GROUP_ERROR_REQUIREMENT_UNMET", value=6),
            PEnumElement(name="SOCIAL_GROUP_ERROR_EMBLEM_INVALID", value=7),
            PEnumElement(name="SOCIAL_GROUP_ERROR_TAG_INVALID", value=8),
            PEnumElement(name="SOCIAL_GROUP_ERROR_TAG_ALREADY_EXISTS", value=9),
            PEnumElement(name="SOCIAL_GROUP_ERROR_UNKNOWN", value=10),
            PEnumElement(name="SOCIAL_GROUP_ON_COOLDOWN", value=11),
        ],
    )
    enum2 = PEnum(
        name="ta",
        elements=[
            PEnumElement(name="SOCIAL_GROUP_OPERATION_OK", value=0),
            PEnumElement(name="SOCIAL_GROUP_ERROR_NAME_INVALID", value=1),
            PEnumElement(name="SOCIAL_GROUP_ERROR_ALREADY_IN_GROUP", value=2),
            PEnumElement(name="SOCIAL_GROUP_ERROR_NAME_ALREADY_EXISTS", value=3),
            PEnumElement(name="SOCIAL_GROUP_ERROR_LEAVE", value=4),
            PEnumElement(name="SOCIAL_GROUP_ERROR_CANCEL", value=5),
            PEnumElement(name="SOCIAL_GROUP_ERROR_REQUIREMENT_UNMET", value=6),
            PEnumElement(name="SOCIAL_GROUP_ERROR_EMBLEM_INVALID", value=7),
            PEnumElement(name="SOCIAL_GROUP_ERROR_TAG_INVALID", value=8),
            PEnumElement(name="SOCIAL_GROUP_ERROR_TAG_ALREADY_EXISTS", value=9),
            PEnumElement(name="SOCIAL_GROUP_ERROR_UNKNOWN", value=10),
        ],
    )
    print(PEnumComparator.compare_enum(enum1, enum2))
