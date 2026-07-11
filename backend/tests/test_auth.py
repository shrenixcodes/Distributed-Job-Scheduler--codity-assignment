
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.core.database import Base
from app.core.config import settings

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def async_client():
    engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register_and_login(async_client: AsyncClient):
    # Register a user
    register_response = await async_client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    assert register_response.status_code == 200
    assert "id" in register_response.json()
    
    # Login
    login_response = await async_client.post(
        "/api/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"

