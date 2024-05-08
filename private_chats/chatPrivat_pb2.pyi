from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PeticioMissatge(_message.Message):
    __slots__ = ("id_thread", "missatge", "id_remitent", "id_destinatari")
    ID_THREAD_FIELD_NUMBER: _ClassVar[int]
    MISSATGE_FIELD_NUMBER: _ClassVar[int]
    ID_REMITENT_FIELD_NUMBER: _ClassVar[int]
    ID_DESTINATARI_FIELD_NUMBER: _ClassVar[int]
    id_thread: int
    missatge: str
    id_remitent: int
    id_destinatari: int
    def __init__(self, id_thread: _Optional[int] = ..., missatge: _Optional[str] = ..., id_remitent: _Optional[int] = ..., id_destinatari: _Optional[int] = ...) -> None: ...

class RespostaMissatge(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class Missatge(_message.Message):
    __slots__ = ("id", "id_thread", "missatge", "id_remitent", "id_destinatari")
    ID_FIELD_NUMBER: _ClassVar[int]
    ID_THREAD_FIELD_NUMBER: _ClassVar[int]
    MISSATGE_FIELD_NUMBER: _ClassVar[int]
    ID_REMITENT_FIELD_NUMBER: _ClassVar[int]
    ID_DESTINATARI_FIELD_NUMBER: _ClassVar[int]
    id: int
    id_thread: int
    missatge: str
    id_remitent: int
    id_destinatari: int
    def __init__(self, id: _Optional[int] = ..., id_thread: _Optional[int] = ..., missatge: _Optional[str] = ..., id_remitent: _Optional[int] = ..., id_destinatari: _Optional[int] = ...) -> None: ...

class Client(_message.Message):
    __slots__ = ("id_destinatari",)
    ID_DESTINATARI_FIELD_NUMBER: _ClassVar[int]
    id_destinatari: int
    def __init__(self, id_destinatari: _Optional[int] = ...) -> None: ...
