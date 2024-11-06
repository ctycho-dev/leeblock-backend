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

    class Config:
        env_file = '.env'


settings = Settings()
