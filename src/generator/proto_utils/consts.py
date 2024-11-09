PROTO_BASE_FIELDS: list[str] = [
    "double",
    "float",
    "int32",
    "int64",
    "uint32",
    "uint64",
    "sint32",
    "sint64",
    "fixed32",
    "fixed64",
    "sfixed32",
    "sfixed64",
    "bool",
    "string",
    "bytes",
    "google.protobuf.Any",
]


BLACKLIST_IMPORT_URLS = ["google/protobuf/any.proto"]
