from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import get_settings

from .db import Player


async def init_db():
    client = AsyncIOMotorClient(get_settings().db_url)
    await init_beanie(database=client.db_name, document_models=[Player])
