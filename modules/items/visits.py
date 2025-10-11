"""
modules/items/visits.py
Visit History CRUD operations dengan in-memory storage
"""

import uuid
from typing import Optional, List, Dict
from datetime import datetime, date
from modules.schema.schemas import VisitHistory


# ===== IN-MEMORY STORAGE =====
visits_db: Dict[str, VisitHistory] = {}  # {visit_id: VisitHistory}


# ===== CRUD OPERATIONS =====
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
    """
    CREATE - Buat record riwayat kunjungan
    
    Args:
        queue_id: ID antrean terkait
        patient_id: ID pasien
        patient_name: Nama pasien
        clinic_id: ID klinik
        clinic_name: Nama klinik
        doctor_id: ID dokter
        doctor_name: Nama dokter
        diagnosis: Diagnosis (optional)
        treatment: Treatment/pengobatan (optional)
        notes: Catatan tambahan (optional)
    
    Returns:
        VisitHistory object yang baru dibuat
    """
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
    """
    READ - Ambil visit berdasarkan ID
    
    Args:
        visit_id: ID visit
    
    Returns:
        VisitHistory object atau None jika tidak ditemukan
    """
    return visits_db.get(visit_id)


def read_all_visits(patient_id: Optional[str] = None, 
                   clinic_id: Optional[str] = None,
                   start_date: Optional[date] = None, 
                   end_date: Optional[date] = None) -> List[VisitHistory]:
    """
    READ - Ambil semua riwayat kunjungan dengan filter
    
    Args:
        patient_id: Filter berdasarkan pasien (optional)
        clinic_id: Filter berdasarkan klinik (optional)
        start_date: Filter tanggal mulai (optional)
        end_date: Filter tanggal akhir (optional)
    
    Returns:
        List of VisitHistory objects (sorted by date, newest first)
    """
    visits = list(visits_db.values())
    
    if patient_id:
        visits = [v for v in visits if v.patient_id == patient_id]
    if clinic_id:
        visits = [v for v in visits if v.clinic_id == clinic_id]
    if start_date:
        visits = [v for v in visits if v.visit_date >= start_date.isoformat()]
    if end_date:
        visits = [v for v in visits if v.visit_date <= end_date.isoformat()]
    
    # Sort by visit date (newest first)
    visits.sort(key=lambda x: x.visit_date, reverse=True)
    return visits


def update_visit(visit_id: str, **kwargs) -> Optional[VisitHistory]:
    """
    UPDATE - Update visit history
    
    Args:
        visit_id: ID visit yang akan diupdate
        **kwargs: Field yang akan diupdate
    
    Returns:
        VisitHistory object yang sudah diupdate atau None jika tidak ditemukan
    """
    visit = visits_db.get(visit_id)
    if not visit:
        return None
    
    # Update fields
    for key, value in kwargs.items():
        if hasattr(visit, key) and value is not None:
            setattr(visit, key, value)
    
    return visit


def delete_visit(visit_id: str) -> bool:
    """
    DELETE - Hapus visit history
    
    Args:
        visit_id: ID visit yang akan dihapus
    
    Returns:
        True jika berhasil, False jika tidak ditemukan
    """
    if visit_id in visits_db:
        del visits_db[visit_id]
        return True
    return False


def get_visits_by_queue(queue_id: str) -> Optional[VisitHistory]:
    """
    Ambil visit history berdasarkan queue_id
    
    Args:
        queue_id: ID antrean
    
    Returns:
        VisitHistory object atau None jika tidak ditemukan
    """
    return next((v for v in visits_db.values() if v.queue_id == queue_id), None)