import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Fixture untuk menyediakan TestClient dari FastAPI app"""
    with TestClient(app) as c:
        yield c