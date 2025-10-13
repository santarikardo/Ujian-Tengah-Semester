# 🏥 Hospital Queue Management System

API untuk manajemen antrean pasien rumah sakit menggunakan FastAPI dengan in-memory storage.

## 📋 Project Structure

```
hospital-queue-management/
│
├── main.py                          # Entry point aplikasi
├── requirements.txt                 # Python dependencies
├── README.md                        # Dokumentasi
│
└── modules/
    ├── schema/
    │   └── schemas.py              # Pydantic models
    │
    ├── items/                      # CRUD operations + in-memory storage
    │   ├── users.py               # User CRUD
    │   ├── clinics.py             # Clinic CRUD
    │   ├── doctors.py             # Doctor CRUD
    │   ├── queues.py              # Queue CRUD
    │   └── visits.py              # Visit History CRUD
    │
    └── routes/                     # API endpoints
        ├── auth.py                # Authentication
        ├── clinics.py             # Clinic endpoints
        ├── doctors.py             # Doctor endpoints
        ├── queues.py              # Queue management
        ├── visits.py              # Visit history
        └── statistics.py          # Statistics
```

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Server

```bash
uvicorn main:app --reload
```

Server akan berjalan di: `http://localhost:8000`

### 3. Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📝 Features

### ✅ Authentication
- Register user (Patient/Doctor/Admin)
- Login dengan session token
- Logout
- Role-based access control

### ✅ Clinic Management (Admin only)
- Create clinic
- Read all clinics
- Update clinic
- Delete clinic

### ✅ Doctor Management (Admin only)
- Create doctor
- Read all doctors
- Update doctor
- Delete doctor

### ✅ Queue Management
- Patient register queue
- View queues (role-based)
- Check queue position
- Call patient (Doctor/Admin)
- Complete service (Doctor/Admin)
- Cancel queue

### ✅ Visit History
- Auto-create when service completed
- View history (role-based)
- Filter by date, patient, clinic

### ✅ Statistics (Doctor/Admin only)
- Queue summary
- Clinic density
- Daily visits

## 🔐 User Roles

| Role | Permissions |
|------|-------------|
| **Patient** | Register queue, view own queues, view own visit history |
| **Doctor** | View all queues in clinic, manage queue status, view all visit history |
| **Admin** | Full access (CRUD clinics/doctors, manage all queues, view all data) |

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Clinics
- `POST /api/clinics` - Create clinic (Admin)
- `GET /api/clinics` - Get all clinics
- `GET /api/clinics/{id}` - Get clinic by ID
- `PUT /api/clinics/{id}` - Update clinic (Admin)
- `DELETE /api/clinics/{id}` - Delete clinic (Admin)

### Doctors
- `POST /api/doctors` - Create doctor (Admin)
- `GET /api/doctors` - Get all doctors
- `GET /api/doctors/{id}` - Get doctor by ID
- `PUT /api/doctors/{id}` - Update doctor (Admin)
- `DELETE /api/doctors/{id}` - Delete doctor (Admin)

### Queues
- `POST /api/queues/register` - Register queue (Patient)
- `GET /api/queues` - Get all queues
- `GET /api/queues/my-position` - Get queue position (Patient)
- `GET /api/queues/{id}` - Get queue by ID
- `PATCH /api/queues/{id}/call` - Call patient (Doctor/Admin)
- `PATCH /api/queues/{id}/complete` - Complete service (Doctor/Admin)
- `PATCH /api/queues/{id}/cancel` - Cancel queue

### Visit History
- `GET /api/visit-history` - Get all visits
- `GET /api/visit-history/{id}` - Get visit by ID

### Statistics
- `GET /api/statistics/queue-summary` - Queue statistics (Doctor/Admin)
- `GET /api/statistics/clinic-density` - Clinic density (Doctor/Admin)
- `GET /api/statistics/daily-visits` - Daily visits (Doctor/Admin)

## 🔧 Development

### Project Requirements (dari dokumen)
- ✅ Tidak menggunakan database
- ✅ Tidak menggunakan JWT
- ✅ Menggunakan struktur data sederhana (dictionary/list)
- ✅ Data tersimpan selama server berjalan
- ✅ Session-based authentication
- ✅ Role-based access control
