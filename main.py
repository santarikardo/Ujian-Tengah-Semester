from fastapi import FastAPI
from modules.routes import auth, clinics, doctors, queues, visits, statistics

app = FastAPI()

# Include all routers
app.include_router(auth.router)
app.include_router(clinics.router)
app.include_router(doctors.router)
app.include_router(queues.router)
app.include_router(visits.router)
app.include_router(statistics.router)