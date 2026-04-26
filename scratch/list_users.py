
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings
from models.user import User

async def list_users():
    client = AsyncIOMotorClient(settings.spring_data_mongodb_uri)
    await init_beanie(database=client[settings.mongodb_database], document_models=[User])
    
    users = await User.find_all().to_list()
    for u in users:
        print(f"ID: {u.id} | Username: {u.username} | Email: {u.email} | Role: {u.role}")

if __name__ == "__main__":
    asyncio.run(list_users())
