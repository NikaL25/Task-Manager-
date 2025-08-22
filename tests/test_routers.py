import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.routers import router
from app.models import Base as ModelBase
from app.deps import get_db

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="module", autouse=True)
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_task(client):
    response = await client.post("/tasks/", json={
        "title": "Test task",
        "description": "Test description",
        "status": "created"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert data["status"] == "created"
    assert "id" in data
    global created_task_id
    created_task_id = data["id"]

@pytest.mark.asyncio
async def test_get_tasks(client):
    response = await client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(task["id"] == created_task_id for task in data)

@pytest.mark.asyncio
async def test_get_task_by_id(client):
    response = await client.get(f"/tasks/{created_task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_task_id
    assert data["title"] == "Test task"

@pytest.mark.asyncio
async def test_update_task(client):
    response = await client.put(f"/tasks/{created_task_id}", json={
        "title": "Updated title",
        "status": "in_progress"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_task_id
    assert data["title"] == "Updated title"
    assert data["status"] == "in_progress"

@pytest.mark.asyncio
async def test_delete_task(client):
    response = await client.delete(f"/tasks/{created_task_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Task deleted"}

    # Проверим, что задачи больше нет
    response = await client.get(f"/tasks/{created_task_id}")
    assert response.status_code == 404
