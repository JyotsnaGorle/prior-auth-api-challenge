from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://priorauth:priorauth@localhost:5432/priorauth"


settings = Settings()
