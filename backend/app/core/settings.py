from pathlib import Path

from pydantic_core import MultiHostUrl
from pydantic import (
    BaseModel,
    RedisDsn,
    PostgresDsn,
    AnyUrl,
    computed_field,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


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

    LOGIN: str
    PASSWORD: str

    @computed_field
    @property
    def REMOTE_DRIVER_URL(self) -> AnyUrl:
        return MultiHostUrl.build(
            scheme="http",
            host="webdriver",
            port=4444,
            path="wd/hub",
        )

    @computed_field
    @property
    def REMOTE_DRIVER_STATUS(self) -> AnyUrl:
        return MultiHostUrl.build(
            scheme="http",
            host="webdriver",
            port=4444,
            path="status",
        )


class AutoCaptcha(BaseSettings):
    model_config = SettingsConfigDict(
        # Dump constants from top level /.env file
        env_file=BASE_DIR / ".env",
        env_prefix="CAPTCHA_",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_KEY: str


class DBSettings(BaseModel):
    POSTGRES_DRIVER: str = "postgresql+asyncpg"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "dev_db"
    ECHO: bool = False  # True only for dev

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.POSTGRES_DRIVER,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


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
    BROKER_PORT: int
    BROKER_PASSWORD: str | None = None
    BROKER_DB: str

    BACKEND_SCHEME: str
    BACKEND_HOST: str
    BACKEND_PORT: int
    BACKEND_PASSWORD: str | None = None
    BACKEND_DB: str

    @computed_field
    @property
    def BROCKER_URL(self) -> RedisDsn:
        return MultiHostUrl.build(
            scheme=self.BROKER_SCHEME,
            # password=self.BROKER_PASSWORD,
            host=self.BROKER_HOST,
            port=self.BROKER_PORT,
            path=self.BROKER_DB,
        )

    @computed_field
    @property
    def BACKEND_URL(self) -> RedisDsn:
        return MultiHostUrl.build(
            scheme=self.BACKEND_SCHEME,
            # password=self.BACKEND_PASSWORD,
            host=self.BACKEND_HOST,
            port=self.BACKEND_PORT,
            path=self.BACKEND_DB,
        )


class Settings(BaseSettings):
    PROJECT_NAME: str = "drone-system"
    API_PREFIX: str = "/api/v1"

    DB: DBSettings = DBSettings()

    GONETS: Gonets = Gonets()
    CELERY: Celery = Celery()
    CAPTCHA: AutoCaptcha = AutoCaptcha()


settings = Settings()
