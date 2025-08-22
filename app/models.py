from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Enum as SQLEnum
from app.database import Base

class TaskStatus(Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    status: TaskStatus = TaskStatus.CREATED

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.CREATED, nullable=False)