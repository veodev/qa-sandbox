import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from config import settings
from dependencies import get_db
from main import app


@pytest_asyncio.fixture(scope="session")
async def engine():
    test_engine = create_async_engine(settings.TEST_DATABASE_URL, poolclass=NullPool)
    yield test_engine
    await test_engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def clean_tables(engine):
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))

    yield


@pytest_asyncio.fixture
async def client(engine):
    async def override_get_db():
        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client

    app.dependency_overrides.clear()


@pytest.fixture
def valid_user():
    return {"email": "test@example.com", "name": "Ivan", "password": "password123"}


@pytest.fixture
def user_with_invalid_email():
    return {"email": "not-an-email", "name": "Ivan", "password": "password123"}
