import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv("DB_USER_NAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv('DB_SERVER_HOST')}:{os.getenv('DB_SERVER_PORT')}/ai_maker_db"

async def get_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

