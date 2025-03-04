from fastapi import HTTPException
import json
from datetime import datetime
from db.connect import get_db_pool
from classes.model import ModelRequest, ModelDeleteRequest
from classes.model import LearningLog

import json

async def get_model_query(conn, model_id: str) -> ModelRequest:
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

    return ModelRequest(
        id=row["id"],
        name=row["name"],
        nn=nn,
        learning_history=learning_history,
        created_at=row["created_at"].isoformat(),
        updated_at=row["updated_at"].isoformat()
    )

async def save_model_query(conn, request: ModelRequest):
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
    
async def update_model_query(conn, request: ModelRequest):
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
            
async def delete_model_query(conn, request: ModelDeleteRequest):
	await conn.execute("""
		DELETE FROM models 
		WHERE id = $1
	""", request.id)