import typing

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class GonetsCookies(BaseModel):
    model_config = ConfigDict(
        extra="ignore", 
        populate_by_name=True,
    )

    username: str = Field(
        ...,
        alias="userNameGS",
        serialization_alias="userNameGS",
    )
    fullname: str = Field(
        ...,
        alias="fullNameGS",
        serialization_alias="fullNameGS",
    )
    login: str = Field(
        ...,
        alias="userLoginGS",
        serialization_alias="userLoginGS",
    )
    client: str = Field(
        ...,
        alias="userClientGS",
        serialization_alias="userClientGS",
    )
    id_session: str = Field(
        ...,
        alias="ASP.NET_SessionId",
        serialization_alias="ASP.NET_SessionId",
    )
    true_user: str = Field(
        ...,
        alias="trueUserV",
        serialization_alias="trueUserV",
    )


class ListMessageHeaders(BaseModel):
    accept_language: str = Field(
        default="en-US,en;q=0.5",
        serialization_alias="Accept-Language",
    )
    accept_encoding: str = Field(
        default="gzip, deflate, br, zstd",
        serialization_alias="Accept-Encoding",
    )
    content_type: str = Field(
        default="application/json; charset=utf-8,",
        serialization_alias="Content-Type",
    )
    accept: str = Field(
        default="application/json, text/javascript, */*; q=0.01",
        serialization_alias="Accept",
    )


class ListMessageBody(BaseModel):
    what: typing.Literal[
        "input",
        "output",
        "send",
        "delete",
    ] = Field(default="send")
    muid: str = Field(default="")
    track: typing.Literal["1", "2"] = Field(default="1")
    uida: str = Field(
        default="",
        serialization_alias="UIDA",
    )
    uid: str = Field(
        default="",
        serialization_alias="ID",
    )
    rc: str = Field(
        default="",
        serialization_alias="Src",
    )
    date_from: str = Field(
        default="",
        serialization_alias="DateFrom",
    )
    date_to: str = Field(
        default="",
        serialization_alias="DateTo",
    )
    no_update: int = Field(
        default=1,
        serialization_alias="noUpdate",
    )
    start_index: str = Field(
        default="0",
        serialization_alias="jtStartIndex",
    )
    page_size: str = Field(
        default="20",
        serialization_alias="jtPageSize",
    )
    sorting: typing.Literal["m_DT DESC"] = Field(
        default="m_DT DESC",
        serialization_alias="jtSorting",
    )
