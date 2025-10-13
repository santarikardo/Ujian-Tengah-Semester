import uuid
from typing import Optional, List, Dict
from datetime import datetime, date
from modules.schema.schemas import VisitHistory


visits_db: Dict[str, VisitHistory] = {}  # {visit_id: VisitHistory}

def create_visit(queue_id: str, 
                patient_id: str, 
                patient_name: str, 
                clinic_id: str, 
                clinic_name: str, 
                doctor_id: str, 
                doctor_name: str,
                diagnosis: Optional[str] = None, 
                treatment: Optional[str] = None, 
                notes: Optional[str] = None) -> VisitHistory:

    visit = VisitHistory(
        id=str(uuid.uuid4()),
        queue_id=queue_id,
        patient_id=patient_id,
        patient_name=patient_name,
        clinic_id=clinic_id,
        clinic_name=clinic_name,
        doctor_id=doctor_id,
        doctor_name=doctor_name,
        visit_date=datetime.now().date().isoformat(),
        diagnosis=diagnosis,
        treatment=treatment,
        notes=notes,
        service_status="selesai"
    )
    
    visits_db[visit.id] = visit
    return visit


def read_visit(visit_id: str) -> Optional[VisitHistory]:
    return visits_db.get(visit_id)


def read_all_visits(patient_id: Optional[str] = None, 
                   clinic_id: Optional[str] = None,
                   start_date: Optional[date] = None, 
                   end_date: Optional[date] = None) -> List[VisitHistory]:
    visits = list(visits_db.values())
    
    if patient_id:
        visits = [v for v in visits if v.patient_id == patient_id]
    if clinic_id:
        visits = [v for v in visits if v.clinic_id == clinic_id]
    if start_date:
        visits = [v for v in visits if v.visit_date >= start_date.isoformat()]
    if end_date:
        visits = [v for v in visits if v.visit_date <= end_date.isoformat()]
    
    visits.sort(key=lambda x: x.visit_date, reverse=True)
    return visits


def update_visit(visit_id: str, **kwargs) -> Optional[VisitHistory]:
    visit = visits_db.get(visit_id)
    if not visit:
        return None
    
    for key, value in kwargs.items():
        if hasattr(visit, key) and value is not None:
            setattr(visit, key, value)
    
    return visit


def delete_visit(visit_id: str) -> bool:
    if visit_id in visits_db:
        del visits_db[visit_id]
        return True
    return False


def get_visits_by_queue(queue_id: str) -> Optional[VisitHistory]:
    return next((v for v in visits_db.values() if v.queue_id == queue_id), None)