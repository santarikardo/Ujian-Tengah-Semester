import pytest
from fastapi.testclient import TestClient
from main import app
from modules.items import users, clinics, doctors, queues, visits

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def clear_all_data():
    users.users_db.clear()
    users.passwords_db.clear()
    users.sessions_db.clear()
    clinics.clinics_db.clear()
    doctors.doctors_db.clear()
    queues.queues_db.clear()
    queues.queue_counters.clear()
    visits.visits_db.clear()
    
    try:
        yield
    finally:
        users.users_db.clear()
        users.passwords_db.clear()
        users.sessions_db.clear()
        clinics.clinics_db.clear()
        doctors.doctors_db.clear()
        queues.queues_db.clear()
        queues.queue_counters.clear()
        visits.visits_db.clear()


@pytest.fixture
def admin_token_header(client):
    client.post("/api/auth/register", json={
        "name": "Admin", "email": "admin@test.com",
        "password": "admin123", "phone": "08123456789", "role": "admin"
    })
    token = client.post("/api/auth/login", json={
        "email": "admin@test.com", "password": "admin123"
    }).json()["session_token"]
    return {"X-Session-Token": token}

@pytest.fixture
def patient_token_header(client):
    client.post("/api/auth/register", json={
        "name": "Patient", "email": "patient@test.com",
        "password": "patient123", "phone": "08123456790", "role": "patient"
    })
    token = client.post("/api/auth/login", json={
        "email": "patient@test.com", "password": "patient123"
    }).json()["session_token"]
    return {"X-Session-Token": token}

@pytest.fixture
def doctor_token_header(client):
    client.post("/api/auth/register", json={
        "name": "Doctor", "email": "doctor@test.com",
        "password": "doctor123", "phone": "08123456791", "role": "doctor"
    })
    token = client.post("/api/auth/login", json={
        "email": "doctor@test.com", "password": "doctor123"
    }).json()["session_token"]
    return {"X-Session-Token": token}
