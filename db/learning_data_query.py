from fastapi import HTTPException
import json
from pydantic import BaseModel
from datetime import datetime
from db.connect import get_db_pool
from typing import List, Union, Optional

class Relevance(BaseModel):
    Q: str
    D: str
    score: float

class Score(BaseModel):
    text: str
    score: float

class LearningData(BaseModel):
    id: str
    name: str
    data: Union[List[Relevance], List[Score]]
    created_at: Optional[str] = None

async def save_learning_data_query(conn, request: LearningData):
    data_json = json.dumps([d.model_dump() for d in request.data])
    print("-- json ---")
    print(data_json)
    await conn.execute("""
        INSERT INTO learning_data (
            id, name, data, created_at
        ) VALUES ($1, $2, $3, $4)
    """,
    request.id,
    request.name,
	data_json,
    datetime.now())
            
async def delete_learning_data_query(conn, id: str):
	await conn.execute("""
		DELETE FROM learning_data
		WHERE id = $1
	""", id)