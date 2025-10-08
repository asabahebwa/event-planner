import asyncio
import pytest
from fastapi.testclient import TestClient
from main import app
from database.connection import Settings
from models.events import Event
from models.users import User


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


async def init_db():
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"
    await test_settings.initialize_database()


@pytest.fixture(scope="session")
def default_client():
    # Initialize database synchronously
    asyncio.run(init_db())
    
    # Use TestClient for FastAPI testing
    with TestClient(app) as client:
        yield client
        # Note: Cleanup is handled by using a test database
