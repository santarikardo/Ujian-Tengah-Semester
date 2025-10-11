"""
tests/conftest.py
Pytest configuration - Versi Sederhana untuk UTS
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from modules.items import users, clinics, doctors, queues, visits

@pytest.fixture
def client():
    """Fixture untuk menyediakan TestClient dari FastAPI app"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clear_all_data():
    """
    Fixture yang otomatis clear semua data sebelum dan sesudah setiap test
    Memastikan setiap test berjalan dengan data bersih
    """
    # Clear before test
    users.users_db.clear()
    users.passwords_db.clear()
    users.sessions_db.clear()
    clinics.clinics_db.clear()
    doctors.doctors_db.clear()
    queues.queues_db.clear()
    queues.queue_counters.clear()
    visits.visits_db.clear()
    
    yield  # Test berjalan di sini
    
    # Clear after test
    users.users_db.clear()
    users.passwords_db.clear()
    users.sessions_db.clear()
    clinics.clinics_db.clear()
    doctors.doctors_db.clear()
    queues.queues_db.clear()
    queues.queue_counters.clear()
    visits.visits_db.clear()


@pytest.fixture
def client():
    """
    Fixture untuk FastAPI TestClient
    Digunakan untuk melakukan HTTP requests ke API
    """
    return TestClient(app)