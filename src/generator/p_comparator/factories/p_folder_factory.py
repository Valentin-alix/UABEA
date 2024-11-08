import os

from proto_schema_parser import Parser

from src.generator.p_comparator.factories.p_file_factory import PFileFactory
from src.generator.p_comparator.models.p_file import PFile
from src.generator.p_comparator.models.p_folder import PFolder


class PFolderFactory:
    @staticmethod
    def create_p_folder(directory: str) -> PFolder:
        files_by_filename: dict[str, PFile] = {}
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                if not filename.endswith(".proto"):
                    continue
                with open(os.path.join(root, filename)) as file:
                    datas = file.read()
                parsed_proto = Parser().parse(datas)
                files_by_filename[filename] = PFileFactory.create_p_file(
                    filename, parsed_proto
                )

        return PFolder(files_by_filename=files_by_filename, root=directory)
