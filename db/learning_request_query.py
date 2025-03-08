import json
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class LayerOrder(BaseModel):
    type: str
    nodes: Optional[int] = None

class LearningRequest(BaseModel):
    id: str
    name: str
    discription: str
    model_orders: List[LayerOrder]
    criterion_order: str
    tokens_length: int
    num_epochs: int
    batch_size: int
    train_data_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

# 保存
async def save_learning_request_query(conn, request: LearningRequest):
    model_orders_json = json.dumps([layer.model_dump() for layer in request.model_orders], indent=2)
    await conn.execute("""
        INSERT INTO learning_requests (
            id, name, discription, model_orders, criterion_order, 
            tokens_length, num_epochs, batch_size, train_data_id, 
            created_at, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    """,
    request.id,
    request.name,
    request.discription,
    model_orders_json,
    request.criterion_order,
    request.tokens_length,
    request.num_epochs, 
    request.batch_size, 
    request.train_data_id,
    datetime.now(), 
    datetime.now())

#更新
async def update_learning_request_query(conn, request: LearningRequest):
    model_orders_json = json.dumps([layer.model_dump() for layer in request.model_orders], indent=2)
    await conn.execute("""
        UPDATE learning_requests 
			SET 
                name = $2,
				discription = $3,
				model_orders = $4, 
				criterion_order = $5,
                tokens_length = $6,
				num_epochs = $7, 
				batch_size = $8, 
				train_data_id = $9, 
				created_at = $10, 
				updated_at = $11
			WHERE id = $1
    """,
    request.id,
    request.name,
    request.discription, 
    model_orders_json,
    request.criterion_order, 
    request.tokens_length,
    request.num_epochs, 
    request.batch_size, 
    request.train_data_id,
    datetime.strptime(request.created_at, "%Y-%m-%d").date(), 
    datetime.now())
    
# 削除
async def delete_learning_request_query(conn, id: str):
	await conn.execute("""
		DELETE FROM learning_requests 
		WHERE id = $1
	""", id)
     
# 取得（1件）
async def get_learning_request_query(conn, request_id: str):
    row = await conn.fetchrow("""
        SELECT *
        FROM learning_requests
        WHERE id = $1
    """, request_id)

    if not row:
        return None

    model_orders = [
        LayerOrder(**layer) for layer in json.loads(row["model_orders"])
    ]

    return LearningRequest(
        id=row["id"],
        name=row["name"],
        discription=row["discription"],
        model_orders=model_orders,
        criterion_order=row["criterion_order"],
        tokens_length=row["tokens_length"],
        num_epochs=row["num_epochs"],
        batch_size=row["batch_size"],
        train_data_id=row["train_data_id"],
        created_at=row["created_at"].isoformat(),
        updated_at=row["updated_at"].isoformat()
    )

# 取得（全件、idのみ）
async def get_all_learning_request_ids_query(conn):
    rows = await conn.fetch("""
        SELECT id, name, discription
        FROM learning_requests
    """)
    
    return rows

            
