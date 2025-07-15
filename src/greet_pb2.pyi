from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NotificationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOTIFICATION_TYPE_UNKNOWN: _ClassVar[NotificationType]
    NOTIFICATION_TYPE_INFO: _ClassVar[NotificationType]
    NOTIFICATION_TYPE_ERROR: _ClassVar[NotificationType]
    NOTIFICATION_TYPE_WARNING: _ClassVar[NotificationType]

class UserActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_ACTION_TYPE_UNKNOWN: _ClassVar[UserActionType]
    USER_ACTION_TYPE_CLICK: _ClassVar[UserActionType]
NOTIFICATION_TYPE_UNKNOWN: NotificationType
NOTIFICATION_TYPE_INFO: NotificationType
NOTIFICATION_TYPE_ERROR: NotificationType
NOTIFICATION_TYPE_WARNING: NotificationType
USER_ACTION_TYPE_UNKNOWN: UserActionType
USER_ACTION_TYPE_CLICK: UserActionType

class GreetMeRequest(_message.Message):
    __slots__ = ("name", "language")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    language: str
    def __init__(self, name: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...

class GreetMeResponse(_message.Message):
    __slots__ = ("greeting",)
    GREETING_FIELD_NUMBER: _ClassVar[int]
    greeting: str
    def __init__(self, greeting: _Optional[str] = ...) -> None: ...

class SubscribeToNotificationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SubscribeToNotificationsResponse(_message.Message):
    __slots__ = ("type", "title", "content", "is_blocking")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    IS_BLOCKING_FIELD_NUMBER: _ClassVar[int]
    type: NotificationType
    title: str
    content: str
    is_blocking: bool
    def __init__(self, type: _Optional[_Union[NotificationType, str]] = ..., title: _Optional[str] = ..., content: _Optional[str] = ..., is_blocking: bool = ...) -> None: ...

class UserActionsRequest(_message.Message):
    __slots__ = ("user_agent", "type", "timestamp")
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    user_agent: str
    type: UserActionType
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, user_agent: _Optional[str] = ..., type: _Optional[_Union[UserActionType, str]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UserActionsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FileUploadRequest(_message.Message):
    __slots__ = ("data", "part_number")
    DATA_FIELD_NUMBER: _ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    part_number: int
    def __init__(self, data: _Optional[bytes] = ..., part_number: _Optional[int] = ...) -> None: ...

class FileUploadResponse(_message.Message):
    __slots__ = ("part_number",)
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    part_number: int
    def __init__(self, part_number: _Optional[int] = ...) -> None: ...
