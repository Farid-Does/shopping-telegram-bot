from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"server_settings": {"search_path": "aiogram"}}
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)