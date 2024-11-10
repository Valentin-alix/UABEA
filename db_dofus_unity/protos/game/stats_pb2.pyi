from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Team(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEAM_CHALLENGER: _ClassVar[Team]
    TEAM_DEFENDER: _ClassVar[Team]
    TEAM_SPECTATOR: _ClassVar[Team]
    TEAM_NEUTRAL: _ClassVar[Team]
TEAM_CHALLENGER: Team
TEAM_DEFENDER: Team
TEAM_SPECTATOR: Team
TEAM_NEUTRAL: Team

class wwr(_message.Message):
    __slots__ = ("esau", "team", "esaw", "esax", "esay", "esaz")
    class Player(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Monster(_message.Message):
        __slots__ = ("esag",)
        ESAG_FIELD_NUMBER: _ClassVar[int]
        esag: int
        def __init__(self, esag: _Optional[int] = ...) -> None: ...
    class Companion(_message.Message):
        __slots__ = ("esak", "esal")
        ESAK_FIELD_NUMBER: _ClassVar[int]
        ESAL_FIELD_NUMBER: _ClassVar[int]
        esak: int
        esal: wwr
        def __init__(self, esak: _Optional[int] = ..., esal: _Optional[_Union[wwr, _Mapping]] = ...) -> None: ...
    class Summon(_message.Message):
        __slots__ = ("esap", "esaq")
        ESAP_FIELD_NUMBER: _ClassVar[int]
        ESAQ_FIELD_NUMBER: _ClassVar[int]
        esap: int
        esaq: wwr
        def __init__(self, esap: _Optional[int] = ..., esaq: _Optional[_Union[wwr, _Mapping]] = ...) -> None: ...
    ESAU_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    ESAW_FIELD_NUMBER: _ClassVar[int]
    ESAX_FIELD_NUMBER: _ClassVar[int]
    ESAY_FIELD_NUMBER: _ClassVar[int]
    ESAZ_FIELD_NUMBER: _ClassVar[int]
    esau: int
    team: Team
    esaw: wwr.Player
    esax: wwr.Monster
    esay: wwr.Companion
    esaz: wwr.Summon
    def __init__(self, esau: _Optional[int] = ..., team: _Optional[_Union[Team, str]] = ..., esaw: _Optional[_Union[wwr.Player, _Mapping]] = ..., esax: _Optional[_Union[wwr.Monster, _Mapping]] = ..., esay: _Optional[_Union[wwr.Companion, _Mapping]] = ..., esaz: _Optional[_Union[wwr.Summon, _Mapping]] = ...) -> None: ...

class wws(_message.Message):
    __slots__ = ("esbe", "esbf", "esbg", "esbh", "esbi", "esbj", "esbk")
    ESBE_FIELD_NUMBER: _ClassVar[int]
    ESBF_FIELD_NUMBER: _ClassVar[int]
    ESBG_FIELD_NUMBER: _ClassVar[int]
    ESBH_FIELD_NUMBER: _ClassVar[int]
    ESBI_FIELD_NUMBER: _ClassVar[int]
    ESBJ_FIELD_NUMBER: _ClassVar[int]
    ESBK_FIELD_NUMBER: _ClassVar[int]
    esbe: int
    esbf: int
    esbg: int
    esbh: int
    esbi: int
    esbj: int
    esbk: int
    def __init__(self, esbe: _Optional[int] = ..., esbf: _Optional[int] = ..., esbg: _Optional[int] = ..., esbh: _Optional[int] = ..., esbi: _Optional[int] = ..., esbj: _Optional[int] = ..., esbk: _Optional[int] = ...) -> None: ...

class FightStats(_message.Message):
    __slots__ = ("damage_done", "damage_taken", "heal_done", "heal_taken", "shield_done", "shield_taken", "eseg", "eseh", "kill", "esej")
    class DamageDone(_message.Message):
        __slots__ = ("esbo", "esbp", "esbq", "esbr", "esbs", "esbt", "esbu", "esbv", "esbw")
        ESBO_FIELD_NUMBER: _ClassVar[int]
        ESBP_FIELD_NUMBER: _ClassVar[int]
        ESBQ_FIELD_NUMBER: _ClassVar[int]
        ESBR_FIELD_NUMBER: _ClassVar[int]
        ESBS_FIELD_NUMBER: _ClassVar[int]
        ESBT_FIELD_NUMBER: _ClassVar[int]
        ESBU_FIELD_NUMBER: _ClassVar[int]
        ESBV_FIELD_NUMBER: _ClassVar[int]
        ESBW_FIELD_NUMBER: _ClassVar[int]
        esbo: int
        esbp: int
        esbq: int
        esbr: int
        esbs: int
        esbt: int
        esbu: float
        esbv: float
        esbw: int
        def __init__(self, esbo: _Optional[int] = ..., esbp: _Optional[int] = ..., esbq: _Optional[int] = ..., esbr: _Optional[int] = ..., esbs: _Optional[int] = ..., esbt: _Optional[int] = ..., esbu: _Optional[float] = ..., esbv: _Optional[float] = ..., esbw: _Optional[int] = ...) -> None: ...
    class DamageTaken(_message.Message):
        __slots__ = ("esca", "escb", "escc", "escd", "esce", "escf", "escg", "esch")
        ESCA_FIELD_NUMBER: _ClassVar[int]
        ESCB_FIELD_NUMBER: _ClassVar[int]
        ESCC_FIELD_NUMBER: _ClassVar[int]
        ESCD_FIELD_NUMBER: _ClassVar[int]
        ESCE_FIELD_NUMBER: _ClassVar[int]
        ESCF_FIELD_NUMBER: _ClassVar[int]
        ESCG_FIELD_NUMBER: _ClassVar[int]
        ESCH_FIELD_NUMBER: _ClassVar[int]
        esca: int
        escb: int
        escc: int
        escd: int
        esce: int
        escf: int
        escg: float
        esch: int
        def __init__(self, esca: _Optional[int] = ..., escb: _Optional[int] = ..., escc: _Optional[int] = ..., escd: _Optional[int] = ..., esce: _Optional[int] = ..., escf: _Optional[int] = ..., escg: _Optional[float] = ..., esch: _Optional[int] = ...) -> None: ...
    class HealDone(_message.Message):
        __slots__ = ("escl", "escm", "escn", "esco")
        ESCL_FIELD_NUMBER: _ClassVar[int]
        ESCM_FIELD_NUMBER: _ClassVar[int]
        ESCN_FIELD_NUMBER: _ClassVar[int]
        ESCO_FIELD_NUMBER: _ClassVar[int]
        escl: int
        escm: int
        escn: float
        esco: float
        def __init__(self, escl: _Optional[int] = ..., escm: _Optional[int] = ..., escn: _Optional[float] = ..., esco: _Optional[float] = ...) -> None: ...
    class HealTaken(_message.Message):
        __slots__ = ("escs", "esct", "escu")
        ESCS_FIELD_NUMBER: _ClassVar[int]
        ESCT_FIELD_NUMBER: _ClassVar[int]
        ESCU_FIELD_NUMBER: _ClassVar[int]
        escs: int
        esct: int
        escu: float
        def __init__(self, escs: _Optional[int] = ..., esct: _Optional[int] = ..., escu: _Optional[float] = ...) -> None: ...
    class ShieldDone(_message.Message):
        __slots__ = ("escy", "escz", "esda")
        ESCY_FIELD_NUMBER: _ClassVar[int]
        ESCZ_FIELD_NUMBER: _ClassVar[int]
        ESDA_FIELD_NUMBER: _ClassVar[int]
        escy: int
        escz: int
        esda: float
        def __init__(self, escy: _Optional[int] = ..., escz: _Optional[int] = ..., esda: _Optional[float] = ...) -> None: ...
    class ShieldTaken(_message.Message):
        __slots__ = ("esde", "esdf", "esdg")
        ESDE_FIELD_NUMBER: _ClassVar[int]
        ESDF_FIELD_NUMBER: _ClassVar[int]
        ESDG_FIELD_NUMBER: _ClassVar[int]
        esde: int
        esdf: int
        esdg: float
        def __init__(self, esde: _Optional[int] = ..., esdf: _Optional[int] = ..., esdg: _Optional[float] = ...) -> None: ...
    class wwt(_message.Message):
        __slots__ = ("esdk", "esdl", "esdm", "esdn", "esdo", "esdp", "esdq")
        ESDK_FIELD_NUMBER: _ClassVar[int]
        ESDL_FIELD_NUMBER: _ClassVar[int]
        ESDM_FIELD_NUMBER: _ClassVar[int]
        ESDN_FIELD_NUMBER: _ClassVar[int]
        ESDO_FIELD_NUMBER: _ClassVar[int]
        ESDP_FIELD_NUMBER: _ClassVar[int]
        ESDQ_FIELD_NUMBER: _ClassVar[int]
        esdk: int
        esdl: int
        esdm: int
        esdn: float
        esdo: float
        esdp: float
        esdq: float
        def __init__(self, esdk: _Optional[int] = ..., esdl: _Optional[int] = ..., esdm: _Optional[int] = ..., esdn: _Optional[float] = ..., esdo: _Optional[float] = ..., esdp: _Optional[float] = ..., esdq: _Optional[float] = ...) -> None: ...
    class Kill(_message.Message):
        __slots__ = ("esdu", "esdv", "esdw")
        ESDU_FIELD_NUMBER: _ClassVar[int]
        ESDV_FIELD_NUMBER: _ClassVar[int]
        ESDW_FIELD_NUMBER: _ClassVar[int]
        esdu: int
        esdv: int
        esdw: int
        def __init__(self, esdu: _Optional[int] = ..., esdv: _Optional[int] = ..., esdw: _Optional[int] = ...) -> None: ...
    DAMAGE_DONE_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_TAKEN_FIELD_NUMBER: _ClassVar[int]
    HEAL_DONE_FIELD_NUMBER: _ClassVar[int]
    HEAL_TAKEN_FIELD_NUMBER: _ClassVar[int]
    SHIELD_DONE_FIELD_NUMBER: _ClassVar[int]
    SHIELD_TAKEN_FIELD_NUMBER: _ClassVar[int]
    ESEG_FIELD_NUMBER: _ClassVar[int]
    ESEH_FIELD_NUMBER: _ClassVar[int]
    KILL_FIELD_NUMBER: _ClassVar[int]
    ESEJ_FIELD_NUMBER: _ClassVar[int]
    damage_done: FightStats.DamageDone
    damage_taken: FightStats.DamageTaken
    heal_done: FightStats.HealDone
    heal_taken: FightStats.HealTaken
    shield_done: FightStats.ShieldDone
    shield_taken: FightStats.ShieldTaken
    eseg: FightStats.wwt
    eseh: FightStats.wwt
    kill: FightStats.Kill
    esej: wwr
    def __init__(self, damage_done: _Optional[_Union[FightStats.DamageDone, _Mapping]] = ..., damage_taken: _Optional[_Union[FightStats.DamageTaken, _Mapping]] = ..., heal_done: _Optional[_Union[FightStats.HealDone, _Mapping]] = ..., heal_taken: _Optional[_Union[FightStats.HealTaken, _Mapping]] = ..., shield_done: _Optional[_Union[FightStats.ShieldDone, _Mapping]] = ..., shield_taken: _Optional[_Union[FightStats.ShieldTaken, _Mapping]] = ..., eseg: _Optional[_Union[FightStats.wwt, _Mapping]] = ..., eseh: _Optional[_Union[FightStats.wwt, _Mapping]] = ..., kill: _Optional[_Union[FightStats.Kill, _Mapping]] = ..., esej: _Optional[_Union[wwr, _Mapping]] = ...) -> None: ...

class ybw(_message.Message):
    __slots__ = ("esen",)
    ESEN_FIELD_NUMBER: _ClassVar[int]
    esen: int
    def __init__(self, esen: _Optional[int] = ...) -> None: ...

class yej(_message.Message):
    __slots__ = ("esez", "esfa")
    class Success(_message.Message):
        __slots__ = ("eser", "eses")
        ESER_FIELD_NUMBER: _ClassVar[int]
        ESES_FIELD_NUMBER: _ClassVar[int]
        eser: int
        eses: int
        def __init__(self, eser: _Optional[int] = ..., eses: _Optional[int] = ...) -> None: ...
    class Error(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    ESEZ_FIELD_NUMBER: _ClassVar[int]
    ESFA_FIELD_NUMBER: _ClassVar[int]
    esez: yej.Success
    esfa: yej.Error
    def __init__(self, esez: _Optional[_Union[yej.Success, _Mapping]] = ..., esfa: _Optional[_Union[yej.Error, _Mapping]] = ...) -> None: ...
