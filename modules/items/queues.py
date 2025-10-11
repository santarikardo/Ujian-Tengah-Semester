"""
modules/items/queues.py
Queue CRUD operations dengan in-memory storage
"""

import uuid
from typing import Optional, List, Dict
from datetime import datetime
from modules.schema.schemas import Queue, QueueStatus


# ===== IN-MEMORY STORAGE =====
queues_db: Dict[str, Queue] = {}  # {queue_id: Queue}
queue_counters: Dict[str, int] = {}  # {clinic_id: counter}


# ===== CRUD OPERATIONS =====
def create_queue(patient_id: str, patient_name: str, clinic_id: str, doctor_id: Optional[str] = None) -> Queue:
    """
    CREATE - Buat antrean baru
    
    Args:
        patient_id: ID pasien
        patient_name: Nama pasien
        clinic_id: ID klinik
        doctor_id: ID dokter (optional)
    
    Returns:
        Queue object yang baru dibuat
    
    Raises:
        ValueError: Jika klinik/dokter tidak valid
    """
    from modules.items.clinics import clinics_db
    from modules.items.doctors import doctors_db
    
    # Validate clinic
    clinic = clinics_db.get(clinic_id)
    if not clinic or not clinic.is_active:
        raise ValueError("Klinik tidak ditemukan atau tidak aktif")
    
    # Validate doctor if provided
    doctor_name = None
    if doctor_id:
        doctor = doctors_db.get(doctor_id)
        if not doctor or not doctor.is_available or doctor.clinic_id != clinic_id:
            raise ValueError("Dokter tidak ditemukan atau tidak tersedia")
        doctor_name = doctor.name
    
    # Generate queue number
    if clinic_id not in queue_counters:
        queue_counters[clinic_id] = 0
    
    queue_counters[clinic_id] += 1
    queue_number = f"{clinic.name[:3].upper()}{queue_counters[clinic_id]:03d}"
    
    queue = Queue(
        id=str(uuid.uuid4()),
        queue_number=queue_number,
        patient_id=patient_id,
        patient_name=patient_name,
        clinic_id=clinic_id,
        clinic_name=clinic.name,
        doctor_id=doctor_id,
        doctor_name=doctor_name,
        status=QueueStatus.WAITING,
        registration_time=datetime.now().isoformat()
    )
    
    queues_db[queue.id] = queue
    return queue


def read_queue(queue_id: str) -> Optional[Queue]:
    """
    READ - Ambil antrean berdasarkan ID
    
    Args:
        queue_id: ID antrean
    
    Returns:
        Queue object atau None jika tidak ditemukan
    """
    return queues_db.get(queue_id)


def read_all_queues(clinic_id: Optional[str] = None, 
                    status: Optional[QueueStatus] = None, 
                    patient_id: Optional[str] = None) -> List[Queue]:
    """
    READ - Ambil semua antrean dengan filter
    
    Args:
        clinic_id: Filter berdasarkan klinik (optional)
        status: Filter berdasarkan status (optional)
        patient_id: Filter berdasarkan pasien (optional)
    
    Returns:
        List of Queue objects (sorted by registration time)
    """
    queues = list(queues_db.values())
    
    if clinic_id:
        queues = [q for q in queues if q.clinic_id == clinic_id]
    if status:
        queues = [q for q in queues if q.status == status]
    if patient_id:
        queues = [q for q in queues if q.patient_id == patient_id]
    
    # Sort by registration time
    queues.sort(key=lambda x: x.registration_time)
    return queues


def update_queue_status(queue_id: str, status: QueueStatus, **kwargs) -> Optional[Queue]:
    """
    UPDATE - Update status antrean
    
    Args:
        queue_id: ID antrean
        status: Status baru
        **kwargs: Field tambahan yang akan diupdate (notes, etc)
    
    Returns:
        Queue object yang sudah diupdate atau None jika tidak ditemukan
    """
    queue = queues_db.get(queue_id)
    if not queue:
        return None
    
    queue.status = status
    
    # Update timestamps based on status
    if status == QueueStatus.IN_SERVICE:
        queue.called_time = datetime.now().isoformat()
        queue.service_start_time = datetime.now().isoformat()
    elif status == QueueStatus.COMPLETED:
        queue.service_end_time = datetime.now().isoformat()
    
    # Update additional fields
    for key, value in kwargs.items():
        if hasattr(queue, key) and value is not None:
            setattr(queue, key, value)
    
    return queue


def delete_queue(queue_id: str) -> bool:
    """
    DELETE - Hapus antrean
    
    Args:
        queue_id: ID antrean yang akan dihapus
    
    Returns:
        True jika berhasil, False jika tidak ditemukan
    """
    if queue_id in queues_db:
        del queues_db[queue_id]
        return True
    return False


def get_queue_position(queue_id: str) -> int:
    """
    Hitung posisi antrean dalam antrian
    
    Args:
        queue_id: ID antrean
    
    Returns:
        Posisi dalam antrian (1-based), atau 0 jika tidak ditemukan
    """
    queue = queues_db.get(queue_id)
    if not queue or queue.status != QueueStatus.WAITING:
        return 0
    
    # Get all waiting queues in the same clinic
    waiting_queues = read_all_queues(
        clinic_id=queue.clinic_id,
        status=QueueStatus.WAITING
    )
    
    # Find position
    for i, q in enumerate(waiting_queues, start=1):
        if q.id == queue_id:
            return i
    
    return 0