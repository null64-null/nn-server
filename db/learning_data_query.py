import json
from pydantic import BaseModel
from datetime import datetime
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

# 保存
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

# 削除
async def delete_learning_data_query(conn, id: str):
	await conn.execute("""
		DELETE FROM learning_data
		WHERE id = $1
	""", id)
     
# 取得（全件、idのみ）
async def get_all_learning_data_ids_query(conn):
    rows = await conn.fetch("""
        SELECT id
        FROM learning_data
    """)
    
    return [row["id"] for row in rows]

# 取得（1件）
async def get_learning_data_query(conn, data_id: str):
    row = await conn.fetchrow("""
        SELECT id, name, data, created_at
        FROM learning_data
        WHERE id = $1
    """, data_id)

    if not row:
        return None

    data = [
        Score(**item) if "text" in item else Relevance(**item)
        for item in json.loads(row["data"])
    ]

    return LearningData(
        id=row["id"],
        name=row["name"],
        data=data,
        created_at=row["created_at"].isoformat()
    )
