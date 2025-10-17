from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    DATABASE_URL: str
    SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str


settings = Settings()
