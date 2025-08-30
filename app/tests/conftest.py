import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from mongomock_motor import AsyncMongoMockClient
import os

os.environ["TESTING"] = "True"

@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)

@pytest.fixture(autouse=True)
async def mock_db():
    """Mock do MongoDB para testes"""
    from app.database import get_db
    import app.main as main
    
    # Usar mongomock para testes
    mock_client = AsyncMongoMockClient()
    mock_db = mock_client.epi_inventory_db
    
    # Sobrescrever a dependência do banco
    async def get_test_db():
        return mock_db
    
    app.dependency_overrides[get_db] = get_test_db
    yield mock_db
    app.dependency_overrides = {}
