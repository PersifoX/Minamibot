"""Config module."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the bot"""

    discord_token: str

    minecraft_server_ip: str
    minecraft_server_port: int
    minecraft_server_password: str

    minecraft_server_url: str

    guild_id: int
    channel_id: int | None = None
    role_id: int | None = None
    customer_role_id: int | None = None

    db_url: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
