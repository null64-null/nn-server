from fastapi import HTTPException
from db.connect import get_db_pool
from classes.model import LearningRequest

async def save_learning_request_query(request: LearningRequest):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            await conn.execute("""
                INSERT INTO learning_requests (
                    id, input_size, model_orders, criterion_order, 
                    num_epochs, batch_size, train_data_id, 
                    test_data_id, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            """,
            request.id, 
            request.input_size, 
            [order.model_dump() for order in request.model_orders], # JSONB に変換
            request.criterion_order, 
            request.num_epochs, 
            request.batch_size, 
            request.train_data_id, 
            request.test_data_id, 
            request.created_at, 
            request.updated_at)
            return {"message": "Data saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            await pool.close()

async def update_learning_request_query(request: LearningRequest):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
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
			[order.model_dump() for order in request.model_orders], # JSONB に変換
			request.criterion_order, 
			request.num_epochs, 
			request.batch_size, 
			request.train_data_id, 
			request.test_data_id, 
			request.created_at, 
			request.updated_at)
            return {"message": "Data update successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            await pool.close()
            
async def delete_learning_request_query(request: LearningRequest):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            await conn.execute("""
				DELETE FROM learning_requests 
				WHERE id = $1
			""", request.id)
            return {"message": "Data delete successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            await pool.close()
