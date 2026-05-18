from functools import cached_property, lru_cache

from pydantic import Field, BaseModel
from pydantic_settings import (BaseSettings,
                               SettingsConfigDict,
                               PydanticBaseSettingsSource,
                               YamlConfigSettingsSource)


class YamlSettings(BaseSettings):
    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


class DatabaseConnectionSettings(BaseModel):
    pool_pre_ping: bool = True
    pool_recycle: int = 1800
    pool_timeout: int = 30
    pool_size: int = 20
    max_overflow: int = 10
    timeout: int | float = 10


class DatabaseSettings(YamlSettings):
    host: str = Field(..., examples=['host'])
    port: int = Field(5432, ge=1, le=65535)
    user: str
    db_name: str
    db_schema: str

    connection: DatabaseConnectionSettings

    model_config = SettingsConfigDict(
        yaml_file='/etc/org_api_app/settings/database_settings.yaml'
    )

    @cached_property
    def password(self) -> str:
        path = '/run/secrets/org_api_app_db_password'
        with open(path, 'r') as f:
            password = f.read().strip()
        return password

    @property
    def url(self):
        return (
            'postgresql+asyncpg://'
            f'{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
        )

@lru_cache
def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()
