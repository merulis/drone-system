from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra=True,
    )

    MQTT_BROKER_HOST: str
    MQTT_BROKER_PORT: int
    MQTT_BROKER_USER: str
    MQTT_BROKER_PASSWORD: str


settings = Settings()
