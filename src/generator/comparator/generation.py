from proto_schema_parser.generator import Generator
from src.generator.comparator.models.mapping_info import MappingInfo


def get_new_file_generated(
    self, mapping_info_by_name: dict[str, MappingInfo]
) -> dict[str, str]:
    generated_file_by_name: dict[str, str] = {}
    new_mapping_name_found: list[str] = [
        map_info.name_with_index[1] for map_info in mapping_info_by_name.values()
    ]

    for index, new_proto_file_info in enumerate(self.new_proto_files_infos.values()):
        found_unknown_msg: bool = False
        for new_msg in new_proto_file_info.messages:
            if new_msg.name in new_mapping_name_found:
                continue
            found_unknown_msg = True
            mapping_info_by_name[new_msg.name] = MappingInfo(
                name_with_index=(index, new_msg.name), similarity=1
            )
        if found_unknown_msg:
            generated_file_by_name[new_proto_file_info.filename] = Generator().generate(
                new_proto_file_info.origin_file
            )
            print(f"New file wille be generated : {new_proto_file_info.filename}")

    return generated_file_by_name
