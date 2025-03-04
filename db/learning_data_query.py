from fastapi import HTTPException
import json
from datetime import datetime
from db.connect import get_db_pool
from classes.data import LearningDataRequest, LearningDataDeleteRequest

async def save_learning_data_query(conn, request: LearningDataRequest):
    data_json = [d.model_dump() for d in request.data]
    await conn.execute("""
        INSERT INTO learinig_data (
            id, name, data, created_at
        ) VALUES ($1, $2, $3, $4)
    """,
    request.id,
    request.name,
	data_json,
    datetime.strptime(request.created_at, "%Y-%m-%d").date())
            
async def delete_learning_data_query(conn, request: LearningDataDeleteRequest):
	await conn.execute("""
		DELETE FROM learinig_data 
		WHERE id = $1
	""", request.id)