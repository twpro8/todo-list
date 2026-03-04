from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")

    APP_NAME: str
    API_V1_STR: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    CORS_ORIGINS: list[str]


settings = Settings()  # type: ignore
