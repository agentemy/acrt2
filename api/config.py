from dataclasses import dataclass
from environs import Env

@dataclass
class DatabaseConfig:
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str


@dataclass
class Config:
    db: DatabaseConfig



def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    db_conf = DatabaseConfig(
        db_user=env("POSTGRES_USER"),
        db_pass=env("POSTGRES_PASSWORD"),
        db_host=env("POSTGRES_HOST"),
        db_port=env("POSTGRES_PORT"),
        db_name=env("POSTGRES_DB")
    )

    return Config(
        db=db_conf,
    )