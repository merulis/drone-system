from dataclasses import dataclass, field
import typing


T = typing.TypeVar("T", bound="DictMixin")


@dataclass
class DictMixin:
    def model_dump(
        self,
        metadata: bool = True,
    ) -> dict:
        """
        Serializes the dataclass instance into a dictionary,
        using metadata keys if provided.
        """
        result = {}

        for data_field in self.__dataclass_fields__.values():
            key = (
                data_field.metadata.get("key", data_field.name)
                if metadata
                else data_field.name
            )
            value = getattr(self, data_field.name)
            if value is not None:
                result[key] = value

        return result

    @classmethod
    def model_from_dict(
        cls: typing.Type[T],
        data: dict,
        metadata: bool = True,
    ) -> T:
        """
        Creates an instance of the dataclass from a data dictionary.

        Args:
            data (dict): The input data dictionary.
            metadata (bool): If True, uses the field's metadata key ("key")
                from metadata["key"]. If False, uses the field's name.

        Returns:
            T: A new instance of the class.
        """
        instance = cls.__new__(cls)

        for data_field in cls.__dataclass_fields__.values():
            key = (
                data_field.metadata.get("key", data_field.name)
                if metadata
                else data_field.name
            )
            if key in data:
                if not isinstance(data[key], data_field.type):
                    t_expected = data_field.type
                    field = data_field.name
                    t_got = type(data[key])
                    raise TypeError(
                        f"Expected {t_expected} for field {field}, got {t_got}"
                    )
                setattr(instance, data_field.name, data[key])

        return instance


@dataclass
class GonetsCookies(DictMixin):
    username: str = field(metadata={"key": "userNameGS"})
    fullname: str = field(metadata={"key": "fullNameGS"})
    login: str = field(metadata={"key": "userLoginGS"})
    client: str = field(metadata={"key": "userClientGS"})
    id_session: str = field(metadata={"key": "ASP.NET_SessionId"})
    true_user: str = field(metadata={"key": "trueUserV"})


@dataclass
class ListMessageHeaders(DictMixin):
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
class ListMessageBody(DictMixin):
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
    uid: str = field(
        default="",
        metadata={"key": "ID"},
    )
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
