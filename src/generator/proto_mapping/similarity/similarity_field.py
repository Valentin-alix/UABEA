from proto_schema_parser import Field

from src.generator.proto_mapping.similarity.consts import PROTO_BASE_FIELDS


def compare_fields(field1: Field, field2: Field) -> float:
    similarity_score: float = 1
    coeff_check_failed: float = 1

    if field1.number != field2.number:
        coeff_check_failed += 1

    if field1.type not in PROTO_BASE_FIELDS:
        if field2.type in PROTO_BASE_FIELDS:
            return 0
    elif field1.type != field2.type:
        coeff_check_failed += 2

    return similarity_score / coeff_check_failed
