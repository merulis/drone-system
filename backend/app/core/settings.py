from pathlib import Path

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
    IMG_FOLDER: Path = Path(__file__).parent.parent.parent / "captcha_img"


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


class Settings(BaseSettings):
    CAPTCHA: AutoCaptcha = AutoCaptcha()
    MQTT: Mqtt = Mqtt()
    GONETS: Gonets = Gonets()


settings = Settings()
