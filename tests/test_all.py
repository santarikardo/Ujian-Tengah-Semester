"""
tests/test_api.py
Unit Tests untuk Hospital Queue Management System
Versi Sederhana - Cukup untuk memenuhi requirement UTS
"""

import pytest


# ====================== SYSTEM HEALTH TESTS ======================
class TestSystem:
    """Test basic system endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint bisa diakses"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Hospital Queue Management System API" in response.json()["message"]
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


# ====================== AUTHENTICATION TESTS ======================
class TestAuthentication:
    """Test authentication: register, login, logout"""
    
    def test_register_patient_success(self, client):
        """Test register patient berhasil"""
        response = client.post("/api/auth/register", json={
            "name": "Test Patient",
            "email": "patient@test.com",
            "password": "password123",
            "phone": "08123456789",
            "role": "patient"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Registrasi berhasil"
        assert data["user"]["role"] == "patient"
        assert data["user"]["medical_record_number"] is not None
    
    def test_login_success(self, client):
        """Test login berhasil setelah register"""
        # Register
        client.post("/api/auth/register", json={
            "name": "Test User",
            "email": "user@test.com",
            "password": "password123",
            "phone": "08123456789",
            "role": "patient"
        })
        
        # Login
        response = client.post("/api/auth/login", json={
            "email": "user@test.com",
            "password": "password123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "session_token" in data
        assert data["user"]["email"] == "user@test.com"
    
    def test_login_wrong_password(self, client):
        """Test login dengan password salah"""
        # Register
        client.post("/api/auth/register", json={
            "name": "Test User",
            "email": "user@test.com",
            "password": "password123",
            "phone": "08123456789",
            "role": "patient"
        })
        
        # Login dengan password salah
        response = client.post("/api/auth/login", json={
            "email": "user@test.com",
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401


# ====================== CLINIC TESTS ======================
class TestClinics:
    """Test CRUD operations untuk Clinic"""
    
    def test_create_clinic(self, client):
        """Test CREATE clinic (Admin only)"""
        # Setup admin
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        # Create clinic
        response = client.post(
            "/api/clinics",
            headers={"X-Session-Token": token},
            json={"name": "Klinik Umum", "description": "Klinik untuk pemeriksaan umum"}
        )
        
        assert response.status_code == 201
        assert response.json()["clinic"]["name"] == "Klinik Umum"
    
    def test_get_all_clinics(self, client):
        """Test READ all clinics"""
        response = client.get("/api/clinics")
        
        assert response.status_code == 200
        assert "clinics" in response.json()
        assert "total" in response.json()
    
    def test_update_clinic(self, client):
        """Test UPDATE clinic"""
        # Setup
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        clinic = client.post(
            "/api/clinics",
            headers={"X-Session-Token": token},
            json={"name": "Klinik Test"}
        ).json()["clinic"]
        
        # Update
        response = client.put(
            f"/api/clinics/{clinic['id']}",
            headers={"X-Session-Token": token},
            json={"name": "Klinik Updated"}
        )
        
        assert response.status_code == 200
        assert response.json()["clinic"]["name"] == "Klinik Updated"
    
    def test_delete_clinic(self, client):
        """Test DELETE clinic"""
        # Setup
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        clinic = client.post(
            "/api/clinics",
            headers={"X-Session-Token": token},
            json={"name": "Klinik Test"}
        ).json()["clinic"]
        
        # Delete
        response = client.delete(
            f"/api/clinics/{clinic['id']}",
            headers={"X-Session-Token": token}
        )
        
        assert response.status_code == 200
        assert "berhasil dihapus" in response.json()["message"]


# ====================== DOCTOR TESTS ======================
class TestDoctors:
    """Test CRUD operations untuk Doctor"""
    
    def test_create_doctor(self, client):
        """Test CREATE doctor"""
        # Setup admin dan clinic
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        clinic = client.post(
            "/api/clinics",
            headers={"X-Session-Token": token},
            json={"name": "Klinik Test"}
        ).json()["clinic"]
        
        # Create doctor
        response = client.post(
            "/api/doctors",
            headers={"X-Session-Token": token},
            json={
                "name": "Dr. Ahmad",
                "specialization": "Dokter Umum",
                "clinic_id": clinic["id"],
                "phone": "08123456789"
            }
        )
        
        assert response.status_code == 201
        assert response.json()["doctor"]["name"] == "Dr. Ahmad"
    
    def test_get_all_doctors(self, client):
        """Test READ all doctors"""
        response = client.get("/api/doctors")
        
        assert response.status_code == 200
        assert "doctors" in response.json()
    
    def test_update_doctor(self, client):
        """Test UPDATE doctor"""
        # Setup
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        clinic = client.post(
            "/api/clinics",
            headers={"X-Session-Token": token},
            json={"name": "Klinik Test"}
        ).json()["clinic"]
        
        doctor = client.post(
            "/api/doctors",
            headers={"X-Session-Token": token},
            json={
                "name": "Dr. Test",
                "specialization": "Dokter Umum",
                "clinic_id": clinic["id"],
                "phone": "08123456789"
            }
        ).json()["doctor"]
        
        # Update
        response = client.put(
            f"/api/doctors/{doctor['id']}",
            headers={"X-Session-Token": token},
            json={"name": "Dr. Updated"}
        )
        
        assert response.status_code == 200
        assert response.json()["doctor"]["name"] == "Dr. Updated"
    
    def test_delete_doctor(self, client):
        """Test DELETE doctor"""
        # Setup
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        clinic = client.post(
            "/api/clinics",
            headers={"X-Session-Token": token},
            json={"name": "Klinik Test"}
        ).json()["clinic"]
        
        doctor = client.post(
            "/api/doctors",
            headers={"X-Session-Token": token},
            json={
                "name": "Dr. Test",
                "specialization": "Dokter Umum",
                "clinic_id": clinic["id"],
                "phone": "08123456789"
            }
        ).json()["doctor"]
        
        # Delete
        response = client.delete(
            f"/api/doctors/{doctor['id']}",
            headers={"X-Session-Token": token}
        )
        
        assert response.status_code == 200


# ====================== QUEUE MANAGEMENT TESTS ======================
class TestQueueManagement:
    """Test queue management: register, call, complete"""
    
    def test_patient_register_queue(self, client):
        """Test patient bisa register queue"""
        # Setup: admin, clinic, patient
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        admin_token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        clinic = client.post(
            "/api/clinics",
            headers={"X-Session-Token": admin_token},
            json={"name": "Klinik Test"}
        ).json()["clinic"]
        
        client.post("/api/auth/register", json={
            "name": "Patient", "email": "patient@test.com",
            "password": "patient123", "phone": "08123456790", "role": "patient"
        })
        patient_token = client.post("/api/auth/login", json={
            "email": "patient@test.com", "password": "patient123"
        }).json()["session_token"]
        
        # Register queue
        response = client.post(
            "/api/queues/register",
            headers={"X-Session-Token": patient_token},
            json={"clinic_id": clinic["id"]}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["queue"]["status"] == "menunggu"
        assert "queue_number" in data["queue"]
    
    def test_complete_queue_flow(self, client):
        """Test complete flow: register -> call -> complete"""
        # Setup: admin, clinic, doctor, patient
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        admin_token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        clinic = client.post(
            "/api/clinics",
            headers={"X-Session-Token": admin_token},
            json={"name": "Klinik Test"}
        ).json()["clinic"]
        
        client.post("/api/auth/register", json={
            "name": "Patient", "email": "patient@test.com",
            "password": "patient123", "phone": "08123456790", "role": "patient"
        })
        patient_token = client.post("/api/auth/login", json={
            "email": "patient@test.com", "password": "patient123"
        }).json()["session_token"]
        
        client.post("/api/auth/register", json={
            "name": "Doctor", "email": "doctor@test.com",
            "password": "doctor123", "phone": "08123456791", "role": "doctor"
        })
        doctor_token = client.post("/api/auth/login", json={
            "email": "doctor@test.com", "password": "doctor123"
        }).json()["session_token"]
        
        # 1. Register queue
        queue_response = client.post(
            "/api/queues/register",
            headers={"X-Session-Token": patient_token},
            json={"clinic_id": clinic["id"]}
        )
        queue = queue_response.json()["queue"]
        assert queue["status"] == "menunggu"
        
        # 2. Call queue
        call_response = client.patch(
            f"/api/queues/{queue['id']}/call",
            headers={"X-Session-Token": doctor_token}
        )
        assert call_response.status_code == 200
        assert call_response.json()["queue"]["status"] == "sedang_dilayani"
        
        # 3. Complete queue
        complete_response = client.patch(
            f"/api/queues/{queue['id']}/complete?diagnosis=Flu&treatment=Paracetamol",
            headers={"X-Session-Token": doctor_token}
        )
        assert complete_response.status_code == 200
        assert complete_response.json()["queue"]["status"] == "selesai"
        assert "visit_history" in complete_response.json()


# ====================== VISIT HISTORY TESTS ======================
class TestVisitHistory:
    """Test visit history functionality"""
    
    def test_visit_history_auto_created(self, client):
        """Test visit history otomatis dibuat saat queue complete"""
        # Setup lengkap
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        admin_token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        clinic = client.post(
            "/api/clinics",
            headers={"X-Session-Token": admin_token},
            json={"name": "Klinik Test"}
        ).json()["clinic"]
        
        client.post("/api/auth/register", json={
            "name": "Patient", "email": "patient@test.com",
            "password": "patient123", "phone": "08123456790", "role": "patient"
        })
        patient_token = client.post("/api/auth/login", json={
            "email": "patient@test.com", "password": "patient123"
        }).json()["session_token"]
        
        client.post("/api/auth/register", json={
            "name": "Doctor", "email": "doctor@test.com",
            "password": "doctor123", "phone": "08123456791", "role": "doctor"
        })
        doctor_token = client.post("/api/auth/login", json={
            "email": "doctor@test.com", "password": "doctor123"
        }).json()["session_token"]
        
        # Register and complete queue
        queue = client.post(
            "/api/queues/register",
            headers={"X-Session-Token": patient_token},
            json={"clinic_id": clinic["id"]}
        ).json()["queue"]
        
        client.patch(
            f"/api/queues/{queue['id']}/call",
            headers={"X-Session-Token": doctor_token}
        )
        
        client.patch(
            f"/api/queues/{queue['id']}/complete?diagnosis=Flu&treatment=Istirahat",
            headers={"X-Session-Token": doctor_token}
        )
        
        # Check visit history
        response = client.get(
            "/api/visit-history",
            headers={"X-Session-Token": patient_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["visit_history"][0]["diagnosis"] == "Flu"


# ====================== STATISTICS TESTS ======================
class TestStatistics:
    """Test statistics endpoints"""
    
    def test_queue_summary(self, client):
        """Test queue summary statistics"""
        # Setup admin
        client.post("/api/auth/register", json={
            "name": "Admin", "email": "admin@test.com",
            "password": "admin123", "phone": "08123456789", "role": "admin"
        })
        admin_token = client.post("/api/auth/login", json={
            "email": "admin@test.com", "password": "admin123"
        }).json()["session_token"]
        
        # Get statistics
        response = client.get(
            "/api/statistics/queue-summary",
            headers={"X-Session-Token": admin_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "total_queues" in data
        assert "waiting" in data
        assert "completed" in data
        assert "average_service_time_minutes" in data