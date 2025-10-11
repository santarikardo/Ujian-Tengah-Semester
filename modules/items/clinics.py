"""
modules/items/clinics.py
Clinic CRUD operations dengan in-memory storage
"""

import uuid
from typing import Optional, List, Dict
from datetime import datetime
from modules.schema.schemas import Clinic


# ===== IN-MEMORY STORAGE =====
clinics_db: Dict[str, Clinic] = {}  # {clinic_id: Clinic}


# ===== CRUD OPERATIONS =====
def create_clinic(name: str, description: Optional[str] = None) -> Clinic:
    """
    CREATE - Buat klinik baru
    
    Args:
        name: Nama klinik
        description: Deskripsi klinik (optional)
    
    Returns:
        Clinic object yang baru dibuat
    """
    clinic = Clinic(
        id=str(uuid.uuid4()),
        name=name,
        description=description,
        is_active=True,
        created_at=datetime.now().isoformat()
    )
    
    clinics_db[clinic.id] = clinic
    return clinic


def read_clinic(clinic_id: str) -> Optional[Clinic]:
    """
    READ - Ambil klinik berdasarkan ID
    
    Args:
        clinic_id: ID klinik
    
    Returns:
        Clinic object atau None jika tidak ditemukan
    """
    return clinics_db.get(clinic_id)


def read_all_clinics(is_active: Optional[bool] = None) -> List[Clinic]:
    """
    READ - Ambil semua klinik dengan optional filter
    
    Args:
        is_active: Filter berdasarkan status aktif (optional)
    
    Returns:
        List of Clinic objects
    """
    clinics = list(clinics_db.values())
    if is_active is not None:
        clinics = [c for c in clinics if c.is_active == is_active]
    return clinics


def update_clinic(clinic_id: str, **kwargs) -> Optional[Clinic]:
    """
    UPDATE - Update klinik
    
    Args:
        clinic_id: ID klinik yang akan diupdate
        **kwargs: Field yang akan diupdate (name, description, is_active)
    
    Returns:
        Clinic object yang sudah diupdate atau None jika tidak ditemukan
    """
    clinic = clinics_db.get(clinic_id)
    if not clinic:
        return None
    
    # Update fields
    for key, value in kwargs.items():
        if hasattr(clinic, key) and value is not None:
            setattr(clinic, key, value)
    
    return clinic


def delete_clinic(clinic_id: str) -> bool:
    """
    DELETE - Hapus klinik
    
    Args:
        clinic_id: ID klinik yang akan dihapus
    
    Returns:
        True jika berhasil
    
    Raises:
        ValueError: Jika masih ada dokter di klinik tersebut
    """
    # Import doctors_db untuk check constraint
    from modules.items.doctors import doctors_db
    
    # Check if there are doctors in this clinic
    doctors_in_clinic = [d for d in doctors_db.values() if d.clinic_id == clinic_id]
    if doctors_in_clinic:
        raise ValueError("Tidak dapat menghapus klinik yang masih memiliki dokter")
    
    if clinic_id in clinics_db:
        del clinics_db[clinic_id]
        return True
    return False