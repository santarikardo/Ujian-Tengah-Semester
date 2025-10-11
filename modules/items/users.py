"""
modules/items/users.py
User CRUD operations dengan in-memory storage
"""

import uuid
import hashlib
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from modules.schema.schemas import User, UserRole


# ===== IN-MEMORY STORAGE =====
users_db: Dict[str, User] = {}  # {user_id: User}
passwords_db: Dict[str, str] = {}  # {user_id: hashed_password}
sessions_db: Dict[str, Dict] = {}  # {session_token: {user_id, expires_at}}


# ===== HELPER FUNCTIONS =====
def hash_password(password: str) -> str:
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_session_token() -> str:
    """Generate session token unik"""
    return str(uuid.uuid4())


# ===== CRUD OPERATIONS =====
def create_user(name: str, email: str, password: str, phone: str, role: UserRole = UserRole.PATIENT) -> User:
    """
    CREATE - Buat user baru
    
    Args:
        name: Nama user
        email: Email user (harus unique)
        password: Password (akan di-hash)
        phone: Nomor telepon
        role: Role user (patient/doctor/admin)
    
    Returns:
        User object yang baru dibuat
    
    Raises:
        ValueError: Jika email sudah terdaftar
    """
    # Check if email exists
    if any(u.email == email for u in users_db.values()):
        raise ValueError("Email sudah terdaftar")
    
    user_id = str(uuid.uuid4())
    
    # Generate Medical Record Number untuk pasien
    medical_record_number = None
    if role == UserRole.PATIENT:
        patient_count = len([u for u in users_db.values() if u.role == UserRole.PATIENT])
        medical_record_number = f"MR{patient_count + 1:06d}"
    
    user = User(
        id=user_id,
        name=name,
        email=email,
        phone=phone,
        role=role,
        medical_record_number=medical_record_number,
        created_at=datetime.now().isoformat()
    )
    
    # Save to storage
    users_db[user_id] = user
    passwords_db[user_id] = hash_password(password)
    
    return user


def read_user(user_id: str) -> Optional[User]:
    """
    READ - Ambil user berdasarkan ID
    
    Args:
        user_id: ID user
    
    Returns:
        User object atau None jika tidak ditemukan
    """
    return users_db.get(user_id)


def read_user_by_email(email: str) -> Optional[User]:
    """
    READ - Ambil user berdasarkan email
    
    Args:
        email: Email user
    
    Returns:
        User object atau None jika tidak ditemukan
    """
    return next((u for u in users_db.values() if u.email == email), None)


def read_all_users(role: Optional[UserRole] = None) -> List[User]:
    """
    READ - Ambil semua user dengan optional filter role
    
    Args:
        role: Filter berdasarkan role (optional)
    
    Returns:
        List of User objects
    """
    users = list(users_db.values())
    if role:
        users = [u for u in users if u.role == role]
    return users


def update_user(user_id: str, **kwargs) -> Optional[User]:
    """
    UPDATE - Update user
    
    Args:
        user_id: ID user yang akan diupdate
        **kwargs: Field yang akan diupdate
    
    Returns:
        User object yang sudah diupdate atau None jika tidak ditemukan
    """
    user = users_db.get(user_id)
    if not user:
        return None
    
    # Update fields
    for key, value in kwargs.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)
    
    return user


def delete_user(user_id: str) -> bool:
    """
    DELETE - Hapus user
    
    Args:
        user_id: ID user yang akan dihapus
    
    Returns:
        True jika berhasil, False jika user tidak ditemukan
    """
    if user_id in users_db:
        del users_db[user_id]
        if user_id in passwords_db:
            del passwords_db[user_id]
        return True
    return False


def verify_password(user_id: str, password: str) -> bool:
    """
    Verifikasi password user
    
    Args:
        user_id: ID user
        password: Password yang akan diverifikasi
    
    Returns:
        True jika password benar, False jika salah
    """
    return passwords_db.get(user_id) == hash_password(password)


# ===== SESSION MANAGEMENT =====
def create_session(user_id: str) -> tuple[str, datetime]:
    """
    Buat session baru untuk user
    
    Args:
        user_id: ID user
    
    Returns:
        Tuple (session_token, expires_at)
    """
    session_token = generate_session_token()
    expires_at = datetime.now() + timedelta(hours=24)
    
    sessions_db[session_token] = {
        "user_id": user_id,
        "expires_at": expires_at
    }
    
    return session_token, expires_at


def verify_session(session_token: str) -> Optional[User]:
    """
    Verifikasi session dan return user
    
    Args:
        session_token: Session token
    
    Returns:
        User object atau None jika session invalid/expired
    """
    if session_token not in sessions_db:
        return None
    
    session = sessions_db[session_token]
    
    # Check if expired
    if datetime.now() > session["expires_at"]:
        del sessions_db[session_token]
        return None
    
    return read_user(session["user_id"])


def delete_session(session_token: str) -> bool:
    """
    Hapus session (logout)
    
    Args:
        session_token: Session token
    
    Returns:
        True jika berhasil
    """
    if session_token in sessions_db:
        del sessions_db[session_token]
        return True
    return False