import os
import asyncpg

DATABASE_URL = f"postgresql:/{os.getenv("DB_USER_NAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv('DB_SERVER_HOST')}/ai_maker_db"

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)
