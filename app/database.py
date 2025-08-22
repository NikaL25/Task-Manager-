import os
from dotenv import load_dotenv

ENV = os.getenv("ENVIRONMENT", "local")  

if ENV == "docker":
    load_dotenv(".env")          
else:
    load_dotenv(".env.local")   

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URL_Local")

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
