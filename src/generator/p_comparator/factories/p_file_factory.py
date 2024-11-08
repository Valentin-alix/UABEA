from proto_schema_parser import Message
from proto_schema_parser.ast import File, Import, Package, Enum, Comment

from src.generator.p_comparator.exceptions import UnhandledTypeCase
from src.generator.p_comparator.factories.p_enum_factory import PEnumFactory
from src.generator.p_comparator.factories.p_message_factory import PMessageFactory
from src.generator.p_comparator.models.p_enum import PEnum
from src.generator.p_comparator.models.p_file import PFile
from src.generator.p_comparator.models.p_message import PMessage


class PFileFactory:
    @staticmethod
    def create_p_file(filename: str, proto_file: File) -> PFile:
        imports: list[str] = []
        p_messages: list[PMessage] = []
        p_enums: list[PEnum] = []
        package: str | None = None
        for file_element in proto_file.file_elements:
            if type(file_element) is Import:
                imports.append(file_element.name)
            elif type(file_element) is Package:
                package = file_element.name
            elif type(file_element) is Message:
                p_messages.append(PMessageFactory.create_p_message(file_element))
            elif type(file_element) is Enum:
                p_enums.append(PEnumFactory.create_p_enum(file_element))
            elif type(file_element) is Comment:
                pass
            else:
                raise UnhandledTypeCase(type(file_element))

        return PFile(
            filename=filename,
            package=package,
            imports=imports,
            messages=p_messages,
            enums=p_enums,
        )
