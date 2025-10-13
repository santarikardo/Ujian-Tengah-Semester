import uuid
from typing import Optional, List, Dict
from datetime import datetime
from modules.schema.schemas import Doctor


doctors_db: Dict[str, Doctor] = {}

def create_doctor(name: str, specialization: str, clinic_id: str, phone: str) -> Doctor:
    
    from modules.items.clinics import clinics_db
    
    clinic = clinics_db.get(clinic_id)
    if not clinic:
        raise ValueError("Clinic not found")
    
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
    return doctors_db.get(doctor_id)


def read_all_doctors(clinic_id: Optional[str] = None, is_available: Optional[bool] = None) -> List[Doctor]:
    doctors = list(doctors_db.values())
    
    if clinic_id:
        doctors = [d for d in doctors if d.clinic_id == clinic_id]
    if is_available is not None:
        doctors = [d for d in doctors if d.is_available == is_available]
    
    return doctors


def update_doctor(doctor_id: str, **kwargs) -> Optional[Doctor]:
    doctor = doctors_db.get(doctor_id)
    if not doctor:
        return None
    
    if "clinic_id" in kwargs and kwargs["clinic_id"]:
        from modules.items.clinics import clinics_db
        clinic = clinics_db.get(kwargs["clinic_id"])
        if not clinic:
            raise ValueError("Clinic not found")
        kwargs["clinic_name"] = clinic.name
    
    for key, value in kwargs.items():
        if hasattr(doctor, key) and value is not None:
            setattr(doctor, key, value)
    
    return doctor


def delete_doctor(doctor_id: str) -> bool:
    if doctor_id in doctors_db:
        del doctors_db[doctor_id]
        return True
    return False