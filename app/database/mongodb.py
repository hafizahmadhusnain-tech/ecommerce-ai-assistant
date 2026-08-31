from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_mongo = MongoDB()

async def connect_to_mongo():
    try:
        db_mongo.client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=2000)
        db_mongo.db = db_mongo.client[settings.MONGODB_DB_NAME]
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"[MongoDB Notice] MongoDB not available ({str(e)}). Chat history running in memory mode.")

async def close_mongo_connection():
    try:
        if db_mongo.client:
            db_mongo.client.close()
            print("MongoDB connection closed.")
    except Exception:
        pass