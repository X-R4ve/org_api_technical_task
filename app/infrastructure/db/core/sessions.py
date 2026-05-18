from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, \
    async_sessionmaker

from app.infrastructure.settings.database_settings import get_db_settings


@lru_cache
def get_async_engine() -> AsyncEngine:
    return create_async_engine(
        url=get_db_settings().url,
        pool_pre_ping=get_db_settings().connection.pool_pre_ping,
        pool_recycle=get_db_settings().connection.pool_recycle,
        pool_size=get_db_settings().connection.pool_size,
        max_overflow=get_db_settings().connection.max_overflow,
        connect_args={
            'command_timeout': get_db_settings().connection.timeout,
            'server_settings': {
                'search_path': get_db_settings().db_schema
            }
        },
        hide_parameters=True
    )


@lru_cache
def get_async_session_maker() -> async_sessionmaker:
    return async_sessionmaker(bind=get_async_engine())
