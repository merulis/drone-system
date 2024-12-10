from dataclasses import dataclass, field
import typing


class ADictMixin:
    def to_dict(self):
        result = {}

        for data_field in self.__dataclass_fields__.values():
            key = data_field.metadata.get("key", data_field.name)
            value = getattr(self, data_field.name)
            result.setdefault(key, value)

        return result


@dataclass
class ListMessageHeaders(ADictMixin):
    accept_language: str = field(
        default="en-US,en;q=0.5",
        metadata={"key": "Accept-Language"},
    )
    accept_encoding: str = field(
        default="gzip, deflate, br, zstd",
        metadata={"key": "Accept-Encoding"},
    )
    content_type: str = field(
        default="application/json; charset=utf-8,",
        metadata={"key": "Content-Type"},
    )
    accept: str = field(
        default="application/json, text/javascript, */*; q=0.01",
        metadata={"key": "Accept"},
    )


@dataclass
class ListMessageBody(ADictMixin):
    what: typing.Literal[
        "input",
        "output",
        "send",
        "delete",
    ] = field(default="send")
    muid: str = field(default="")
    track: typing.Literal["1", "2"] = field(default="1")
    uida: str = field(
        default="",
        metadata={"key": "UIDA"},
    )
    uid: str = field(default="", metadata={"key": "ID"},)
    src: str = field(default="", metadata={"key": "Src"})
    date_from: str = field(
        default="",
        metadata={"key": "DateFrom"},
    )
    date_to: str = field(
        default="",
        metadata={"key": "DateTo"},
    )
    no_update: int = field(
        default=1,
        metadata={"key": "noUpdate"},
    )
    start_index: str = field(
        default="0",
        metadata={"key": "jtStartIndex"},
    )
    page_size: str = field(
        default="20",
        metadata={"key": "jtPageSize"},
    )
    sorting: typing.Literal["m_DT DESC"] = field(
        default="m_DT DESC",
        metadata={"key": "jtSorting"},
    )


MyDataClasses = typing.Union[ListMessageBody, ListMessageHeaders]
