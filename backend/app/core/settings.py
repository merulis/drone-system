from pathlib import Path

from pydantic_core import MultiHostUrl
from pydantic import RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent.parent.parent


class Gonets(BaseSettings):
    model_config = SettingsConfigDict(
        # Dump constants from top level /.env file
        env_file=BASE_DIR / ".env",
        env_prefix="GONETS_",
        env_ignore_empty=True,
        extra="ignore",
    )

    BASE_URL: str
    LOGIN_ROUTE: str
    MAIN_ROUTE: str

    LIST_MESSAGE_ROUTE: str
    LIST_MESSAGE_JSON: dict = {
        "what": "send",
        "muid": "",
        "track": "1",
        "UIDA": "",
        "Src": "",
        "DateFrom": "",
        "DateTo": "",
        "noUpdate": 1,
        "ID": "",
        "jtStartIndex": "0",
        "jtPageSize": "20",
        "jtSorting": "m_DT DESC",
    }
    LIST_MESSAGE_USER_ID: str = "ID"
    COOKIE_USER_LOGIN: str = "userLoginGS"

    LOGIN: str
    PASSWORD: str


class AutoCaptcha(BaseSettings):
    model_config = SettingsConfigDict(
        # Dump constants from top level /.env file
        env_file=BASE_DIR / ".env",
        env_prefix="CAPTCHA_",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_KEY: str


class Mqtt(BaseSettings):
    model_config = SettingsConfigDict(
        # Dump constants from top level /.env file
        env_file=BASE_DIR / ".env",
        env_prefix="MQTT_",
        env_ignore_empty=True,
        extra="ignore",
    )

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str


class Celery(BaseSettings):
    model_config = SettingsConfigDict(
        # Dump constants from top level /.env file
        env_file=BASE_DIR / ".env",
        env_prefix="CELERY_",
        env_ignore_empty=True,
        extra="ignore",
    )

    BROKER_SCHEME: str
    BROKER_HOST: str
    BROKER_PORT: str
    BROKER_PASSWORD: str
    BROKER_DB: str

    BACKEND_SCHEME: str
    BACKEND_HOST: str
    BACKEND_PORT: str
    BACKEND_PASSWORD: str
    BACKEND_DB: str

    @computed_field
    @property
    def BROCKER_URL(self) -> RedisDsn:
        return MultiHostUrl.build(
            scheme=self.BROKER_SCHEME,
            password=self.BROKER_PASSWORD,
            host=self.BROKER_HOST,
            port=self.BROKER_PORT,
            path=self.BROKER_DB,
        )

    @computed_field
    @property
    def BACKEND_URL(self) -> RedisDsn:
        return MultiHostUrl.build(
            scheme=self.BROKER_SCHEME,
            password=self.BROKER_PASSWORD,
            host=self.BROKER_HOST,
            port=self.BROKER_PORT,
            path=self.BROKER_DB,
        )


class Settings(BaseSettings):
    CELERY: Celery = Celery()
    CAPTCHA: AutoCaptcha = AutoCaptcha()
    MQTT: Mqtt = Mqtt()
    GONETS: Gonets = Gonets()


settings = Settings()
