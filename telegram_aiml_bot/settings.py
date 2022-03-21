from xmlrpc.client import Boolean
from pydantic import BaseSettings, Field
from typing import (List)

import telegram

class Settings(BaseSettings):
    token: str = Field(env="TELEGRAM_BOT_TOKEN")
    admins: List[int] = Field(env="LIST_OF_ADMINS")
    use_telegram_callback: Boolean = Field(env="USE_TELEGRAM_CALLBACK")
    telegram_callback_url: str = Field(env="TELEGRAM_CALLBACK_URL")
    telegram_callback_port: int = Field(env="TELEGRAM_CALLBACK_PORT")

    class Config:
        env_file = ".env"

settings = Settings()