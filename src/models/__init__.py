from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .db import Player


async def init_db():
    client = AsyncIOMotorClient("mongodb://mongodb:27017")
    await init_beanie(database=client.db_name, document_models=[Player])
