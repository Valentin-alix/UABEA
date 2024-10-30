from dataclasses import dataclass, field

from proto_schema_parser.ast import Import, Package, Enum, Message, File


@dataclass
class ProtoFileInfo:
    origin_file: File
    filename: str
    imports: list[Import] = field(default_factory=lambda: [])
    package: Package | None = field(default=None)
    messages: list[Message] = field(default_factory=lambda: [])
    enums: list[Enum] = field(default_factory=lambda: [])
