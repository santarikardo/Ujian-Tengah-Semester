import uuid
import hashlib
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from modules.schema.schemas import User, UserRole


users_db: Dict[str, User] = {}  # {user_id: User}
passwords_db: Dict[str, str] = {}  # {user_id: hashed_password}
sessions_db: Dict[str, Dict] = {}  # {session_token: {user_id, expires_at}}


def hash_password(password: str) -> str:
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_session_token() -> str:
    """Generate session token unik"""
    return str(uuid.uuid4())


# ===== CRUD OPERATIONS =====
def create_user(name: str, email: str, password: str, phone: str, role: UserRole = UserRole.PATIENT) -> User:
    if any(u.email == email for u in users_db.values()):
        raise ValueError("Email sudah terdaftar")
    
    user_id = str(uuid.uuid4())
    
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
    
    users_db[user_id] = user
    passwords_db[user_id] = hash_password(password)
    
    return user


def read_user(user_id: str) -> Optional[User]:
    return users_db.get(user_id)


def read_user_by_email(email: str) -> Optional[User]:
    return next((u for u in users_db.values() if u.email == email), None)


def read_all_users(role: Optional[UserRole] = None) -> List[User]:
    users = list(users_db.values())
    if role:
        users = [u for u in users if u.role == role]
    return users


def update_user(user_id: str, **kwargs) -> Optional[User]:
    user = users_db.get(user_id)
    if not user:
        return None
    
    
    for key, value in kwargs.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)
    
    return user


def delete_user(user_id: str) -> bool:
    if user_id in users_db:
        del users_db[user_id]
        if user_id in passwords_db:
            del passwords_db[user_id]
        return True
    return False


def verify_password(user_id: str, password: str) -> bool:
    return passwords_db.get(user_id) == hash_password(password)


def create_session(user_id: str) -> tuple[str, datetime]:
    session_token = generate_session_token()
    expires_at = datetime.now() + timedelta(hours=24)
    
    sessions_db[session_token] = {
        "user_id": user_id,
        "expires_at": expires_at
    }
    
    return session_token, expires_at


def verify_session(session_token: str) -> Optional[User]:
    if session_token not in sessions_db:
        return None
    
    session = sessions_db[session_token]
    
    if datetime.now() > session["expires_at"]:
        del sessions_db[session_token]
        return None
    
    return read_user(session["user_id"])


def delete_session(session_token: str) -> bool:
    if session_token in sessions_db:
        del sessions_db[session_token]
        return True
    return False