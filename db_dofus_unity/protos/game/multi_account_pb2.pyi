import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AutoFollowActivationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AutoFollowActivationResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[AutoFollowActivationResponse.Result]
        ERROR: _ClassVar[AutoFollowActivationResponse.Result]
    SUCCESS: AutoFollowActivationResponse.Result
    ERROR: AutoFollowActivationResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: AutoFollowActivationResponse.Result
    def __init__(self, result: _Optional[_Union[AutoFollowActivationResponse.Result, str]] = ...) -> None: ...

class AutoFollowActivatedEvent(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: _Optional[int] = ...) -> None: ...

class AutoFollowDeactivationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AutoFollowDeactivationResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[AutoFollowDeactivationResponse.Result]
        ERROR: _ClassVar[AutoFollowDeactivationResponse.Result]
    SUCCESS: AutoFollowDeactivationResponse.Result
    ERROR: AutoFollowDeactivationResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: AutoFollowDeactivationResponse.Result
    def __init__(self, result: _Optional[_Union[AutoFollowDeactivationResponse.Result, str]] = ...) -> None: ...

class AutoFollowDeactivatedEvent(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: _Optional[int] = ...) -> None: ...

class LeaderPositionEvent(_message.Message):
    __slots__ = ("player_id", "map", "cell_id")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    CELL_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    map: _common_pb2.MapExtendedCoordinates
    cell_id: int
    def __init__(self, player_id: _Optional[int] = ..., map: _Optional[_Union[_common_pb2.MapExtendedCoordinates, _Mapping]] = ..., cell_id: _Optional[int] = ...) -> None: ...

class FightAutoJoinActivationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FightAutoJoinActivationResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[FightAutoJoinActivationResponse.Result]
        ERROR: _ClassVar[FightAutoJoinActivationResponse.Result]
    SUCCESS: FightAutoJoinActivationResponse.Result
    ERROR: FightAutoJoinActivationResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: FightAutoJoinActivationResponse.Result
    def __init__(self, result: _Optional[_Union[FightAutoJoinActivationResponse.Result, str]] = ...) -> None: ...

class FightAutoJoinActivatedEvent(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: _Optional[int] = ...) -> None: ...

class FightAutoJoinDeactivationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FightAutoJoinDeactivatedResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[FightAutoJoinDeactivatedResponse.Result]
        ERROR: _ClassVar[FightAutoJoinDeactivatedResponse.Result]
    SUCCESS: FightAutoJoinDeactivatedResponse.Result
    ERROR: FightAutoJoinDeactivatedResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: FightAutoJoinDeactivatedResponse.Result
    def __init__(self, result: _Optional[_Union[FightAutoJoinDeactivatedResponse.Result, str]] = ...) -> None: ...

class FightAutoJoinDeactivatedEvent(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: _Optional[int] = ...) -> None: ...

class FightAutoReadyActivationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FightAutoReadyActivationResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[FightAutoReadyActivationResponse.Result]
        ERROR: _ClassVar[FightAutoReadyActivationResponse.Result]
    SUCCESS: FightAutoReadyActivationResponse.Result
    ERROR: FightAutoReadyActivationResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: FightAutoReadyActivationResponse.Result
    def __init__(self, result: _Optional[_Union[FightAutoReadyActivationResponse.Result, str]] = ...) -> None: ...

class FightAutoReadyActivatedEvent(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: _Optional[int] = ...) -> None: ...

class FightAutoReadyDeactivationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FightAutoReadyDeactivationResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[FightAutoReadyDeactivationResponse.Result]
        ERROR: _ClassVar[FightAutoReadyDeactivationResponse.Result]
    SUCCESS: FightAutoReadyDeactivationResponse.Result
    ERROR: FightAutoReadyDeactivationResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: FightAutoReadyDeactivationResponse.Result
    def __init__(self, result: _Optional[_Union[FightAutoReadyDeactivationResponse.Result, str]] = ...) -> None: ...

class FightAutoReadyDeactivatedEvent(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: _Optional[int] = ...) -> None: ...

class cqxn(_message.Message):
    __slots__ = ("eqzx",)
    EQZX_FIELD_NUMBER: _ClassVar[int]
    eqzx: str
    def __init__(self, eqzx: _Optional[str] = ...) -> None: ...

class crid(_message.Message):
    __slots__ = ("erab",)
    ERAB_FIELD_NUMBER: _ClassVar[int]
    erab: int
    def __init__(self, erab: _Optional[int] = ...) -> None: ...
