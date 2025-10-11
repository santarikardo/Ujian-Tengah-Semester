"""
main.py
Hospital Queue Management System - FastAPI Entry Point
"""

from fastapi import FastAPI
from modules.routes import auth, clinics, doctors, queues, visits, statistics
from modules.items.users import users_db
from modules.items.clinics import clinics_db
from modules.items.doctors import doctors_db
from modules.items.queues import queues_db

# Initialize FastAPI app
app = FastAPI(
    title="Hospital Queue Management System",
    description="API untuk manajemen antrean pasien rumah sakit",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include all routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(clinics.router, prefix="/api/clinics", tags=["Clinics"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(queues.router, prefix="/api/queues", tags=["Queue Management"])
app.include_router(visits.router, prefix="/api/visit-history", tags=["Visit History"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["Statistics"])


@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint - Informasi API
    """
    return {
        "message": "Hospital Queue Management System API",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs"
    }


@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint - Status sistem
    """
    from modules.schema.schemas import QueueStatus
    
    active_queues = len([q for q in queues_db.values() 
                        if q.status in [QueueStatus.WAITING, QueueStatus.IN_SERVICE]])
    
    return {
        "status": "healthy",
        "storage_type": "In-Memory",
        "statistics": {
            "total_users": len(users_db),
            "total_clinics": len(clinics_db),
            "total_doctors": len(doctors_db),
            "active_queues": active_queues,
            "total_queues": len(queues_db)
        }
    }


@app.on_event("startup")
async def startup_event():
    """
    Event yang dijalankan saat aplikasi startup
    """
    print("=" * 50)
    print("🏥 Hospital Queue Management System")
    print("=" * 50)
    print("✅ Server started successfully!")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Event yang dijalankan saat aplikasi shutdown
    """
    print("\n" + "=" * 50)
    print("👋 Server shutting down...")
    print("⚠️  WARNING: All data will be lost (in-memory storage)")
    print("=" * 50)


# Run dengan: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)