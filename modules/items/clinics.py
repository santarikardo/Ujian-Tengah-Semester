import uuid
from typing import Optional, List, Dict
from datetime import datetime
from modules.schema.schemas import Clinic
from modules.items.doctors import doctors_db

clinics_db: Dict[str, Clinic] = {}

def create_clinic(name: str, description: Optional[str] = None) -> Clinic:
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
    return clinics_db.get(clinic_id)


def read_all_clinics(is_active: Optional[bool] = None) -> List[Clinic]:
    clinics = list(clinics_db.values())
    if is_active is not None:
        clinics = [c for c in clinics if c.is_active == is_active]
    return clinics


def update_clinic(clinic_id: str, **kwargs) -> Optional[Clinic]:
    clinic = clinics_db.get(clinic_id)
    if not clinic:
        return None
    
    # Update fields
    for key, value in kwargs.items():
        if hasattr(clinic, key) and value is not None:
            setattr(clinic, key, value)
    
    return clinic


def delete_clinic(clinic_id: str) -> bool:
    doctors_in_clinic = [d for d in doctors_db.values() if d.clinic_id == clinic_id]
    if doctors_in_clinic:
        raise ValueError("Tidak dapat menghapus klinik yang masih memiliki dokter")
    
    if clinic_id in clinics_db:
        del clinics_db[clinic_id]
        return True
    return False