"""
modules/items/doctors.py
Doctor CRUD operations dengan in-memory storage
"""

import uuid
from typing import Optional, List, Dict
from datetime import datetime
from modules.schema.schemas import Doctor


# ===== IN-MEMORY STORAGE =====
doctors_db: Dict[str, Doctor] = {}  # {doctor_id: Doctor}


# ===== CRUD OPERATIONS =====
def create_doctor(name: str, specialization: str, clinic_id: str, phone: str) -> Doctor:
    """
    CREATE - Buat dokter baru
    
    Args:
        name: Nama dokter
        specialization: Spesialisasi dokter
        clinic_id: ID klinik
        phone: Nomor telepon
    
    Returns:
        Doctor object yang baru dibuat
    
    Raises:
        ValueError: Jika klinik tidak ditemukan
    """
    # Import clinics_db untuk validasi
    from modules.items.clinics import clinics_db
    
    # Validate clinic exists
    clinic = clinics_db.get(clinic_id)
    if not clinic:
        raise ValueError("Klinik tidak ditemukan")
    
    doctor = Doctor(
        id=str(uuid.uuid4()),
        name=name,
        specialization=specialization,
        clinic_id=clinic_id,
        clinic_name=clinic.name,
        phone=phone,
        is_available=True,
        created_at=datetime.now().isoformat()
    )
    
    doctors_db[doctor.id] = doctor
    return doctor


def read_doctor(doctor_id: str) -> Optional[Doctor]:
    """
    READ - Ambil dokter berdasarkan ID
    
    Args:
        doctor_id: ID dokter
    
    Returns:
        Doctor object atau None jika tidak ditemukan
    """
    return doctors_db.get(doctor_id)


def read_all_doctors(clinic_id: Optional[str] = None, is_available: Optional[bool] = None) -> List[Doctor]:
    """
    READ - Ambil semua dokter dengan optional filter
    
    Args:
        clinic_id: Filter berdasarkan klinik (optional)
        is_available: Filter berdasarkan ketersediaan (optional)
    
    Returns:
        List of Doctor objects
    """
    doctors = list(doctors_db.values())
    
    if clinic_id:
        doctors = [d for d in doctors if d.clinic_id == clinic_id]
    if is_available is not None:
        doctors = [d for d in doctors if d.is_available == is_available]
    
    return doctors


def update_doctor(doctor_id: str, **kwargs) -> Optional[Doctor]:
    """
    UPDATE - Update dokter
    
    Args:
        doctor_id: ID dokter yang akan diupdate
        **kwargs: Field yang akan diupdate
    
    Returns:
        Doctor object yang sudah diupdate atau None jika tidak ditemukan
    
    Raises:
        ValueError: Jika clinic_id baru tidak valid
    """
    doctor = doctors_db.get(doctor_id)
    if not doctor:
        return None
    
    # If clinic_id is being updated, validate and update clinic_name
    if "clinic_id" in kwargs and kwargs["clinic_id"]:
        from modules.items.clinics import clinics_db
        clinic = clinics_db.get(kwargs["clinic_id"])
        if not clinic:
            raise ValueError("Klinik tidak ditemukan")
        kwargs["clinic_name"] = clinic.name
    
    # Update fields
    for key, value in kwargs.items():
        if hasattr(doctor, key) and value is not None:
            setattr(doctor, key, value)
    
    return doctor


def delete_doctor(doctor_id: str) -> bool:
    """
    DELETE - Hapus dokter
    
    Args:
        doctor_id: ID dokter yang akan dihapus
    
    Returns:
        True jika berhasil, False jika dokter tidak ditemukan
    """
    if doctor_id in doctors_db:
        del doctors_db[doctor_id]
        return True
    return False