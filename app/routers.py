from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID, uuid4
from app.models import Task, TaskUpdate, TaskDB, TaskStatus
from app.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

from app.deps import get_db


@router.post("/tasks/", response_model=Task)
async def create_task(task: Task, db: AsyncSession = Depends(get_db)):
    db_task = TaskDB(**task.model_dump()) 
    db_task.id = str(uuid4()) 
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=list[Task])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB))
    tasks = result.scalars().all()
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).filter(TaskDB.id == str(task_id)))
    task = result.scalars().first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: UUID, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).filter(TaskDB.id == str(task_id)))
    task = result.scalars().first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).filter(TaskDB.id == str(task_id)))
    task = result.scalars().first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return {"detail": "Task deleted"}