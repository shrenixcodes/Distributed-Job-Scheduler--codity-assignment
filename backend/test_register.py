
import asyncio
import httpx
import sys
import os
from pathlib import Path

# Add src to path so we can import app
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Remove test database if exists to start fresh
db_path = Path(__file__).parent / "scheduler.db"
if db_path.exists():
    os.remove(db_path)

from app.main import app
from app.core.database import engine, Base

async def test_register_and_login():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        print("Testing registration...")
        response = await client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "test1234",
                "full_name": "Test User"
            }
        )
        print(f"Registration Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Registration Response: {response.json()}")
        
        print("\nTesting login...")
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "test1234"
            }
        )
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Login Response: {response.json()}")

if __name__ == "__main__":
    asyncio.run(test_register_and_login())

