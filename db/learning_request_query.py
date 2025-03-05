from fastapi import HTTPException
import json
from datetime import datetime
from db.connect import get_db_pool
from pydantic import BaseModel
from typing import List, Union, Optional

class LayerOrder(BaseModel):
    type: str
    nodes: Optional[int] = None

class LearningRequest(BaseModel):
    id: str
    name: str
    input_size: int
    model_orders: List[LayerOrder]
    criterion_order: str
    num_epochs: int
    batch_size: int
    train_data_id: str
    test_data_id: str
    created_at: str
    updated_at: str
            
async def save_learning_request_query(conn, request: LearningRequest):
    model_orders_json = json.dumps([layer.model_dump() for layer in request.model_orders], indent=2)
    await conn.execute("""
        INSERT INTO learning_requests (
            id, input_size, model_orders, criterion_order, 
            num_epochs, batch_size, train_data_id, 
            test_data_id, created_at, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
    """,
    request.id, 
    request.input_size, 
    model_orders_json,
    request.criterion_order, 
    request.num_epochs, 
    request.batch_size, 
    request.train_data_id, 
    request.test_data_id, 
    datetime.strptime(request.created_at, "%Y-%m-%d").date(), 
    datetime.strptime(request.updated_at, "%Y-%m-%d").date())
    
async def update_learning_request_query(conn, request: LearningRequest):
    model_orders_json = json.dumps([layer.model_dump() for layer in request.model_orders], indent=2)
    await conn.execute("""
        UPDATE learning_requests 
			SET 
				input_size = $2, 
				model_orders = $3, 
				criterion_order = $4, 
				num_epochs = $5, 
				batch_size = $6, 
				train_data_id = $7, 
				test_data_id = $8, 
				created_at = $9, 
				updated_at = $10
			WHERE id = $1
    """,
    request.id, 
    request.input_size, 
    model_orders_json,
    request.criterion_order, 
    request.num_epochs, 
    request.batch_size, 
    request.train_data_id, 
    request.test_data_id, 
    datetime.strptime(request.created_at, "%Y-%m-%d").date(), 
    datetime.strptime(request.updated_at, "%Y-%m-%d").date())
    
            
async def delete_learning_request_query(conn, id: str):
	await conn.execute("""
		DELETE FROM learning_requests 
		WHERE id = $1
	""", id)
            
