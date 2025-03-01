import os
import asyncpg

DATABASE_URL = f"postgresql:/{os.getenv("DB_USER_NAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv('DB_SERVER_HOST')}/ai_maker_db"

async def get_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

