from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Dump constants from top level /.env file
        env_file=BASE_DIR / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    MQTT_BROKER_HOST: str
    MQTT_BROKER_PORT: int
    MQTT_BROKER_USER: str
    MQTT_BROKER_PASSWORD: str


settings = Settings()

print(settings.MQTT_BROKER_USER)