import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from app.infrastructure.db.core.base import Base
from app.repositories.department_repository import DepartmentRepository


@pytest.fixture(scope='session')
def postgres_container():
    with PostgresContainer(
            image='postgres:18-alpine',
            driver='asyncpg'
    ) as postgres:
        yield postgres


@pytest.fixture(scope='session')
def async_engine(postgres_container):
    return create_async_engine(
        url=postgres_container.get_connection_url()
    )


@pytest.fixture(scope='session')
async def build_database(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



@pytest.fixture(scope='function')
async def async_session_maker(async_engine):
    yield async_sessionmaker(bind=async_engine)

    table_names = ', '.join(f'"{t.name}"' for t in Base.metadata.sorted_tables)
    async with async_engine.begin() as conn:
        await conn.execute(
            text(f'TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE;')
        )


@pytest.fixture(scope='function')
async def async_session(async_session_maker):
    async with async_session_maker() as session:
        yield session


@pytest.fixture
def department_repo(async_session):
    return DepartmentRepository(session=async_session)
