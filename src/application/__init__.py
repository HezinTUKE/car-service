from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
import yaml


class RabbitMQConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    queue: str
    exchange: str
    durable: bool = Field(default=True)


class DatabaseConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    db_name: str


class SecurityConfig(BaseModel):
    secret_key: str
    algorithm: str
    token_expire: int
    refresh_token_expire: int


class OpenSearchConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_ssl: bool = Field(default=True)


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int


class Config(BaseModel):
    environment: str = Field(default="DEV")
    origin: str = Field(default="CarService")
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    opensearch: OpenSearchConfig = Field(default_factory=OpenSearchConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    rabbitmq: RabbitMQConfig = Field(default_factory=RabbitMQConfig)

    model_config = ConfigDict(extra="allow")


CONFIG_PATH = Path(__file__).resolve().parent / "config.yml"


def load_config():
    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)


config = Config(**load_config())
