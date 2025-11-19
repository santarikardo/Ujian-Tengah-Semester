from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class QueueStatus(str, Enum):
    WAITING = "menunggu"
    IN_SERVICE = "sedang_dilayani"
    COMPLETED = "selesai"
    CANCELLED = "dibatalkan"


class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    role: UserRole
    medical_record_number: Optional[str] = None
    created_at: str = Field(
        ...,
        default_factory=lambda: datetime.now().isoformat()
    )


class Clinic(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: str = Field(
        ...,
        default_factory=lambda: datetime.now().isoformat()
    )


class Doctor(BaseModel):
    id: str
    name: str
    specialization: str
    clinic_id: str
    clinic_name: Optional[str] = None
    phone: str
    is_available: bool = True
    created_at: str = Field(
        ...,
        default_factory=lambda: datetime.now().isoformat()
    )


class Queue(BaseModel):
    id: str
    queue_number: str
    patient_id: str
    patient_name: str
    clinic_id: str
    clinic_name: str
    doctor_id: Optional[str] = None
    doctor_name: Optional[str] = None
    status: QueueStatus
    registration_time: str
    called_time: Optional[str] = None
    service_start_time: Optional[str] = None
    service_end_time: Optional[str] = None
    notes: Optional[str] = None


# -------------------- VISIT HISTORY (KUNJUNGAN / APPOINTMENT) --------------------


class VisitHistory(BaseModel):
    """
    Riwayat kunjungan pasien.

    Field-field di bawah ini disesuaikan dengan kolom dataset Kaggle
    "Hospital Management System" (reason, appointment_Date, payment_amount,
    mode_of_payment, mode_of_appointment, appointment_status)
    tapi tetap ditambah informasi dari sistem antrean.
    """

    # identitas record di sistem
    id: str
    queue_id: str

    # identitas pasien & dokter di sistem
    patient_id: str
    patient_name: str
    clinic_id: str
    clinic_name: str
    doctor_id: str
    doctor_name: str

    # tanggal kunjungan / appointment (dipakai juga buat filter)
    visit_date: str = Field(
        ...,
        description="Tanggal kunjungan dalam format ISO yyyy-mm-dd"
    )

    # kolom yang mirip dengan dataset Kaggle
    reason: str
    payment_amount: float
    mode_of_payment: str
    mode_of_appointment: str

    # hasil kunjungan pasien (label ala Kaggle)
    # Completed / Cancelled / Scheduled / No-Show
    appointment_status: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    role: UserRole = UserRole.PATIENT


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ClinicCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ClinicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    clinic_id: str
    phone: str


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    clinic_id: Optional[str] = None
    phone: Optional[str] = None
    is_available: Optional[bool] = None


class QueueRegisterRequest(BaseModel):
    clinic_id: str
    doctor_id: Optional[str] = None


# BODY UNTUK /queues/{id}/complete – PARAMETER DARI DATASET KAGGLE
class CompleteQueueRequest(BaseModel):
    reason: str
    payment_amount: float
    mode_of_payment: str
    mode_of_appointment: str
