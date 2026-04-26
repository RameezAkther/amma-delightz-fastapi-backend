from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings

import logging

logger = logging.getLogger(__name__)

client = None

async def init_db():
    global client
    client = AsyncIOMotorClient(settings.spring_data_mongodb_uri)
    
    # Check if database exists and force creation if not
    try:
        db_names = await client.list_database_names()
        if settings.mongodb_database not in db_names:
            logger.info(f"Database '{settings.mongodb_database}' not found. Initializing...")
            # MongoDB creates a database lazily when the first document/collection is created.
            # We explicitly create a collection to force database physical creation.
            await client[settings.mongodb_database].create_collection("_init")
            logger.info(f"Database '{settings.mongodb_database}' created successfully.")
    except Exception as e:
        logger.warning(f"Could not verify or create database automatically: {e}")
    
    from models.user import User
    from models.recipe import Recipe
    from models.favorite import Favorite
    
    await init_beanie(database=client[settings.mongodb_database], document_models=[User, Recipe, Favorite])
