from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str 
    app_host: str
    app_port: int

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str  
    postgres_port: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def DATABASE_URL_sync(self):
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()