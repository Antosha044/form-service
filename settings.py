from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str 
    app_host: str
    app_port: int
    
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()