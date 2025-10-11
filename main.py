from fastapi import FastAPI
from modules.routes import auth, clinics, doctors, queues, visits, statistics

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