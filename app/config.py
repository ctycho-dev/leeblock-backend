""" Configuration """
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_username: str
    db_password: str
    email_from: str
    email_pwd: str
    email_to: str
    tinkoff_url: str
    terminal_key: str
    terminal_pwd: str
    terminal_desc: str

    class Config:
        env_file = '.env'


settings = Settings()
