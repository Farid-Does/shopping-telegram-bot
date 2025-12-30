import asyncio
from database import engine
from models import Base

async def create_db():
    async with engine.begin() as connection:
        # Create all tables defined in models.py
        await connection.run_sync(Base.metadata.create_all)


asyncio.run(create_db())
