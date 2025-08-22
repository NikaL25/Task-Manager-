# Task Manager API

A simple asynchronous Task Manager API built with FastAPI, async SQLAlchemy, and PostgreSQL.
The project supports both local development and Docker-based deployment, with database migrations managed via Alembic.

---

## Project Overview

This API allows you to manage tasks using typical CRUD operations.
It uses:

## PostgreSQL for persistent data storage

## SQLAlchemy (async) for interacting with the database

## Alembic for managing schema migrations

---

## 🚀 Features

✅ FastAPI-based asynchronous REST API

✅ Async PostgreSQL support using SQLAlchemy + asyncpg

✅ Database migrations with Alembic

✅ Docker support for application and database

✅ Hot-reload for local development

✅ Full Swagger UI documentation

✅ Unit & integration testing with pytest and httpx

✅ Clean, modular, PEP8-compliant codebase

---

##🔧 Prerequisites

Python 3.10+

PostgreSQL (for local development)

Docker & Docker Compose

pip (Python package manager)
---

## 📦 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/NikaL25/Task-Manager-.git
cd Task-Manager-

### 2. Setup Python Virtual Environment
python -m venv venv
# Activate the virtual environment:
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate    

### 3. Install Dependencies
pip install -r requirements.txt


### 4. Configure Environment Variables
## 👉 For Docker deployment

# Create a .env file in the root directory:

## DATABASE_URL=postgresql+asyncpg://postgres:admin@db:5432/taskmanagerdb
## POSTGRES_USER=postgres
##POSTGRES_PASSWORD=admin
## POSTGRES_DB=task_manager_server

## 👉 For Local development
# Create a .env.local file:

## DATABASE_URL_Local=postgresql+asyncpg://postgres:admin@localhost:5432/task_manager_server
Ensure your local PostgreSQL server is running and the database exists (or create it manually).



# Create a .env.local file in the project root with the following variables (example):
##  DATABASE_URL_Local=postgresql+asyncpg://postgres:admin@localhost:5432/task_manager_server


🔄 Database Migrations with Alembic

Alembic is used for managing and applying changes to the database schema.


1. Initialize Alembic (only once)
# alembic init alembic

(Skip this if alembic/ already exists.)

## 2. Create a New Migration

alembic revision --autogenerate -m "Add tasks table"
This will generate a migration script based on the latest changes in your models.

## 3. Apply Migrations
alembic upgrade head
This applies all pending migrations to your database.


### 🖥️ Running the Application
▶️ Local Development (Uvicorn)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Open the interactive API docs at:
👉 http://localhost:8000/docs



### 🐳 Run with Docker

## 1.Build and start containers:

docker-compose up --build

## 2. Open API documentation:

👉 http://localhost:8001/docs

## 3. Stop the containers:

docker-compose down

2. Test the API

Open in your browser:
http://localhost:8001/docs

3. Stop containers
docker-compose down


✅ Running Tests

We use pytest for both unit and integration testing.
# 1. Unit Tests (using in-memory SQLite):
pytest tests/test_routers.py -v


2. Integration Tests (using PostgreSQL via Docker):
pytest tests/test_integration_docker.py -v
Make sure the containers are running if testing against Dockerized DB.



🛠 Highlights

⚡ Asynchronous API using FastAPI + SQLAlchemy

🐘 PostgreSQL for reliable data storage

🐳 Docker for consistent environment setup

🧪 Full testing support (unit + integration)

🔄 Alembic migrations for production-ready DB handling

🧼 Clean, modular, and scalable codebase






