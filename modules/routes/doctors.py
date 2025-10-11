"""
modules/routes/doctors.py
Doctor CRUD endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from modules.schema.schemas import DoctorCreate, DoctorUpdate, User
from modules.items import doctors as doctor_crud
from modules.routes.auth import get_current_user, require_admin

router = APIRouter()


@router.post("", status_code=201)
async def create_doctor(data: DoctorCreate, current_user: User = Depends(require_admin)):
    """
    POST - Tambah dokter baru (Admin only)
    
    Headers:
        X-Session-Token: Admin session token
    
    Request Body:
        - name: Nama dokter
        - specialization: Spesialisasi
        - clinic_id: ID klinik
        - phone: Nomor telepon
    
    Returns:
        Doctor object yang baru dibuat
    """
    try:
        doctor = doctor_crud.create_doctor(
            name=data.name,
            specialization=data.specialization,
            clinic_id=data.clinic_id,
            phone=data.phone
        )
        return {"message": "Dokter berhasil ditambahkan", "doctor": doctor}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
async def get_all_doctors(clinic_id: Optional[str] = None, 
                         is_available: Optional[bool] = None):
    """
    GET - Dapatkan semua dokter
    
    Query Parameters:
        - clinic_id: Filter berdasarkan klinik (optional)
        - is_available: Filter berdasarkan ketersediaan (optional)
    
    Returns:
        List of Doctor objects
    """
    doctors = doctor_crud.read_all_doctors(clinic_id=clinic_id, is_available=is_available)
    return {"doctors": doctors, "total": len(doctors)}


@router.get("/{doctor_id}")
async def get_doctor(doctor_id: str):
    """
    GET - Dapatkan detail dokter berdasarkan ID
    
    Path Parameters:
        - doctor_id: ID dokter
    
    Returns:
        Doctor object
    """
    doctor = doctor_crud.read_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Dokter tidak ditemukan")
    return {"doctor": doctor}


@router.put("/{doctor_id}")
async def update_doctor(doctor_id: str, data: DoctorUpdate,
                       current_user: User = Depends(require_admin)):
    """
    PUT - Update dokter (Admin only)
    
    Headers:
        X-Session-Token: Admin session token
    
    Path Parameters:
        - doctor_id: ID dokter
    
    Request Body:
        - name: Nama dokter baru (optional)
        - specialization: Spesialisasi baru (optional)
        - clinic_id: ID klinik baru (optional)
        - phone: Nomor telepon baru (optional)
        - is_available: Status ketersediaan (optional)
    
    Returns:
        Doctor object yang sudah diupdate
    """
    try:
        doctor = doctor_crud.update_doctor(
            doctor_id=doctor_id,
            name=data.name,
            specialization=data.specialization,
            clinic_id=data.clinic_id,
            phone=data.phone,
            is_available=data.is_available
        )
        if not doctor:
            raise HTTPException(status_code=404, detail="Dokter tidak ditemukan")
        return {"message": "Dokter berhasil diupdate", "doctor": doctor}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: str, current_user: User = Depends(require_admin)):
    """
    DELETE - Hapus dokter (Admin only)
    
    Headers:
        X-Session-Token: Admin session token
    
    Path Parameters:
        - doctor_id: ID dokter
    
    Returns:
        Success message
    """
    success = doctor_crud.delete_doctor(doctor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dokter tidak ditemukan")
    return {"message": "Dokter berhasil dihapus"}