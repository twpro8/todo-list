from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    APP_NAME: str
    API_V1_STR: str
    SQLITE_DB_URL: str

    CORS_ORIGINS: list[str]


settings = Settings()  # type: ignore
