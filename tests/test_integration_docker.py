import asyncio
import pytest
import httpx
import subprocess

@pytest.fixture(scope="module")
def docker_compose_up():
    subprocess.run(["docker-compose", "up", "-d", "--build"], check=True)
    for _ in range(30):  
        try:
            r = httpx.get("http://localhost:8001/docs")
            if r.status_code == 200:
                break
        except Exception:
            pass
        asyncio.sleep(1)
    else:
        subprocess.run(["docker-compose", "logs", "app"])
        subprocess.run(["docker-compose", "down"])
        pytest.fail("Сервис не поднялся за 30 секунд")

    yield

    subprocess.run(["docker-compose", "down"], check=True)

@pytest.mark.asyncio
async def test_create_and_get_task(docker_compose_up):
    async with httpx.AsyncClient(base_url="http://localhost:8001") as client:
        # Создаем задачу
        response = await client.post("/tasks/", json={
            "title": "Docker Task",
            "description": "Test from Docker"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Docker Task"
        task_id = data["id"]

        # Получаем задачу по id
        get_response = await client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        task = get_response.json()
        assert task["id"] == task_id
        assert task["description"] == "Test from Docker"

        list_response = await client.get("/tasks/")
        assert list_response.status_code == 200
        tasks = list_response.json()
        assert any(t["id"] == task_id for t in tasks)
