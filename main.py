from fastapi import FastAPI, Response
from modules.routes import auth, clinics, doctors, queues, visits, statistics
from modules.items.users import users_db
from modules.items.clinics import clinics_db
from modules.items.doctors import doctors_db
from modules.items.queues import queues_db

app = FastAPI(
    title="Hospital Queue Management System",
    description="API for hospital queue management system",
    version="1.2.2",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(clinics.router, prefix="/api/clinics", tags=["Clinics"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(queues.router, prefix="/api/queues", tags=["Queue Management"])
app.include_router(visits.router, prefix="/api/visit-history", tags=["Visit History"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["Statistics"])

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

@app.get("/", tags=["System"])
async def root():
    return {
        "message": "Hospital Queue Management System API",
        "version": "1.2.2",
        "status": "running",
        "documentation": "/docs"
    }

@app.get("/health", tags=["System"])
async def health_check():
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