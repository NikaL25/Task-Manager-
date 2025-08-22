from fastapi import FastAPI
from app.routers import router
from app.database import init_db

app = FastAPI(title="Task Manager API")
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await init_db()