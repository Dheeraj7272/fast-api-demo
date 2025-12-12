from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import Product

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.fast_api_first

    await init_beanie(database=db, document_models=[Product])