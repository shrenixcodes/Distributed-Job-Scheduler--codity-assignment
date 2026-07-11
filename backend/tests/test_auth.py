
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.core.database import Base, get_db

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

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

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


@pytest.mark.asyncio
async def test_authenticated_project_queue_and_job_flow(async_client: AsyncClient):
    await async_client.post(
        "/api/auth/register",
        json={"email": "scheduler@example.com", "password": "testpassword123", "full_name": "Scheduler User"},
    )
    login_response = await async_client.post(
        "/api/auth/login",
        data={"username": "scheduler@example.com", "password": "testpassword123"},
    )
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

    project_response = await async_client.post(
        "/api/projects/", json={"name": "Production"}, headers=headers
    )
    assert project_response.status_code == 200

    queue_response = await async_client.post(
        "/api/queues/",
        json={"name": "notifications", "project_id": project_response.json()["id"], "concurrency_limit": 3},
        headers=headers,
    )
    assert queue_response.status_code == 200

    job_response = await async_client.post(
        "/api/jobs/",
        json={"queue_id": queue_response.json()["id"], "payload": {"message": "hello"}},
        headers=headers,
    )
    assert job_response.status_code == 200
    assert job_response.json()["status"] == "queued"
