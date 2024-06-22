import os
from typing import List

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
ENV_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), ".env.template")


class BotConfig(BaseModel):
    token: str = None
    admins: str = None

    @property
    def admin_ids(self) -> List[int]:
        return [int(admin_id) for admin_id in self.admins.split(",")]


class DatabaseConfig(BaseModel):
    url: PostgresDsn = None
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_TEMPLATE_PATH, ENV_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    bot: BotConfig
    db: DatabaseConfig


settings = Settings()
