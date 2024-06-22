from typing import List

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseModel):
    token: str
    admins: str

    @property
    def admin_ids(self) -> List[int]:
        return [int(admin_id) for admin_id in self.admins.split(",")]


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    bot: BotConfig
    db: DatabaseConfig


settings = Settings()
