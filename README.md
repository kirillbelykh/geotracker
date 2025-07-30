# 📍 GeoTracker

**GeoTracker** is a simple REST API built with FastAPI.  
It allows users to register, log in, and store their GPS coordinates.  
Each user can send their location and then retrieve the latest one or the full location history.

---

## ✅ Features

- User registration and login
- JWT-based authentication
- Save user's location (latitude, longitude, timestamp)
- Get the latest saved location
- Get full location history

---

## 🛠 Tech Stack

- **FastAPI** — modern async web framework
- **PostgreSQL** — database for storing users and locations
- **SQLAlchemy** — ORM for database models
- **Pydantic** — data validation
- **JWT (python-jose)** — for authentication
- **Docker & Docker Compose** — for containerized development
- **Pytest** — for testing
- **GitHub Actions** — continuous integration

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/kirillbelykh/geotracker.git
cd geotracker
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
uvicorn app.main:app --reload
```

Swagger UI:
Open your browser at http://localhost:8000/docs

🐳 Run with Docker

Build and run:
```bash
docker-compose up --build
```

API will be available at:
http://localhost:8000
