import json
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from db.learning_request_query import LearningRequest

import json

class LearningLog(BaseModel):
    accuracy: float
    learning_request: LearningRequest

class Model(BaseModel):
    id: str
    name: str
    nn: bytes
    learning_history: Optional[List[LearningLog]] = []
    created_at: str
    updated_at: str

# 取得（1件）
async def get_model_query(conn, model_id: str):
    row = await conn.fetchrow("""
        SELECT id, name, nn, learning_history, created_at, updated_at
        FROM models
        WHERE id = $1
    """, model_id)

    if not row:
        return None
    
    nn = row["nn"] if row["nn"] else None
    learning_history = [
        LearningLog(**log) for log in json.loads(row["learning_history"])
    ]

    return Model(
        id=row["id"],
        name=row["name"],
        nn=nn,
        learning_history=learning_history,
        created_at=row["created_at"].isoformat(),
        updated_at=row["updated_at"].isoformat()
    )

# 取得（全件、idのみ）
async def get_all_model_ids_query(conn):
    rows = await conn.fetch("""
        SELECT id
        FROM models
    """)
    
    return [row["id"] for row in rows]

# 保存（1件）
async def save_model_query(conn, request: Model):
    learning_history_json = json.dumps([log.model_dump() for log in request.learning_history])  
    await conn.execute("""
        INSERT INTO models (
            id, name, nn, learning_history, created_at, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6)
    """,
    request.id,
    request.name,
    request.nn,
    learning_history_json,
    datetime.strptime(request.created_at, "%Y-%m-%d").date(), 
    datetime.strptime(request.updated_at, "%Y-%m-%d").date())

# 更新
async def update_model_query(conn, request: Model):
    learning_history_json = json.dumps([log.model_dump() for log in request.learning_history]) 
    await conn.execute("""
        UPDATE models 
			SET 
        name = $2,
        nn = $3,
        learning_history = $4,
        created_at = $5,
        updated_at = $6
			WHERE id = $1
    """,
    request.id,
    request.name, 
    request.nn,
    learning_history_json,
    datetime.strptime(request.created_at, "%Y-%m-%d").date(), 
    datetime.strptime(request.updated_at, "%Y-%m-%d").date())

# 削除
async def delete_model_query(conn, id: str):
	await conn.execute("""
		DELETE FROM models 
		WHERE id = $1
	""", id)