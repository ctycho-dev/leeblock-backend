""" Configuration """
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # FastAPI
    host: str
    port: int
    # Redis
    redis_host: str
    redis_port: int
    mode: str
    # Database
    db_hostname: str
    db_port: str
    db_name: str
    db_username: str
    db_password: str
    # Email
    email_from: str
    email_pwd: str
    email_to: str
    # CDEK
    cdek_endpoint: str
    cdek_grant_type: str
    cdek_client_id: str
    cdek_client_secret: str
    # Tinkoff
    tinkoff_url: str
    terminal_key: str
    terminal_pwd: str
    terminal_desc: str

    class Config:
        env_file = '.env'


settings = Settings()
