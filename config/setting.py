from environs import Env
from typing import Literal
from pydantic.v1 import BaseSettings, root_validator, validator
env = Env()
environment: Literal["docker", "local"] = "docker"
if environment == "docker":
    env.read_env(path="./docker/.env")
else:
    env.read_env(path=".env")


class Setting(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    PSQL_HOST: str
    PSQL_PORT: str
    POSTGRES_DB: str
    BUILD_URL: str = None
    BOT_TOKEN: str
    ADMINS: str | list[str]

    @root_validator()
    def build_url(cls, values):
        if not values["BUILD_URL"]:
            values["BUILD_URL"] = (
                f"postgresql+psycopg2://{values['POSTGRES_USER']}:"
                f"{values['POSTGRES_PASSWORD']}@{values['PSQL_HOST']}:"
                f"{values['PSQL_PORT']}/{values['POSTGRES_DB']}"
            )

        return values

    @validator("ADMINS")
    def int_to_list(cls, values):
        if isinstance(values, str):
            values = values.split(",")
        return values


setting = Setting()
