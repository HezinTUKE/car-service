from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    ENVIRONMENT: str = "DEV"
    ORIGIN: str = "CarService"

    # POSTGRES
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_TOKEN_EXPIRATION: int

    # RABBIT
    AMQP_USERNAME: str
    AMQP_PASSWORD: str
    AMQP_HOST: str
    AMQP_PORT: int
    AMQP_EXCHANGE: str

    # AWS
    AWS_PROFILE: str
    AWS_BUCKET_NAME: str
    AWS_COGNITO_APP_CLIENT_ID: str
    AWS_COGNITO_APP_CLIENT_SECRET: str
    AWS_USER_POOL_ID: str
    AWS_REGION: str
    AWS_COGNITO_DOMAIN: str
    AWS_COGNITO_SIGNING_KEY_URL: str

    # STRIPE
    STRIPE_API_KEY: str
    STRIPE_SECRET_KEY: str

    @computed_field
    @property
    def DB_URL(self) -> str:
        return f"""postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"""


settings = Settings()
