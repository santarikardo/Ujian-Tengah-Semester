"""
modules/routes/auth.py
Authentication endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from modules.schema.schemas import RegisterRequest, LoginRequest, User, UserRole
from modules.items import users as user_crud

router = APIRouter()


# ===== DEPENDENCIES =====
async def get_current_user(session_token: Optional[str] = Header(None, alias="X-Session-Token")) -> User:
    """
    Dependency untuk mendapatkan user yang sedang login
    
    Args:
        session_token: Session token dari header
    
    Returns:
        User object
    
    Raises:
        HTTPException: Jika session invalid atau expired
    """
    if not session_token:
        raise HTTPException(status_code=401, detail="Session token required")
    
    user = user_crud.verify_session(session_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return user


async def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency yang require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


async def require_doctor_or_admin(current_user: User = Depends(get_current_user)):
    """Dependency yang require doctor atau admin role"""
    if current_user.role not in [UserRole.DOCTOR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Doctor or admin access required")
    return current_user


# ===== ENDPOINTS =====
@router.post("/register", status_code=201)
async def register(req: RegisterRequest):
    """
    POST - Register user baru
    
    Request Body:
        - name: Nama lengkap
        - email: Email (harus unique)
        - password: Password
        - phone: Nomor telepon
        - role: patient/doctor/admin (default: patient)
    
    Returns:
        User object yang baru dibuat
    """
    try:
        user = user_crud.create_user(
            name=req.name,
            email=req.email,
            password=req.password,
            phone=req.phone,
            role=req.role
        )
        return {"message": "Registrasi berhasil", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(req: LoginRequest):
    """
    POST - Login dan dapatkan session token
    
    Request Body:
        - email: Email user
        - password: Password user
    
    Returns:
        Session token dan informasi user
    """
    # Verify user
    user = user_crud.read_user_by_email(req.email)
    if not user or not user_crud.verify_password(user.id, req.password):
        raise HTTPException(status_code=401, detail="Email atau password salah")
    
    # Create session
    session_token, expires_at = user_crud.create_session(user.id)
    
    return {
        "message": "Login berhasil",
        "session_token": session_token,
        "user": user,
        "expires_at": expires_at.isoformat()
    }


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user),
                session_token: str = Header(..., alias="X-Session-Token")):
    """
    POST - Logout dan hapus session
    
    Headers:
        X-Session-Token: Session token
    
    Returns:
        Success message
    """
    user_crud.delete_session(session_token)
    return {"message": "Logout berhasil"}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """
    GET - Dapatkan informasi user yang sedang login
    
    Headers:
        X-Session-Token: Session token
    
    Returns:
        User object
    """
    return {"user": current_user}