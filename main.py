import io
from fastapi import FastAPI, Query
from fastapi import HTTPException
import uuid
import datetime
from pydantic import BaseModel

from classes.api_request import CreateLearningDataRequest, DeleteRequest, GetRequest
from generate_model.learning import generate_model
from generate_data.prompt import prompt_relevance, prompt_score, make_json
from generate_data.groq import get_completion
from db.connect import get_db_pool
from db.learning_request_query import save_learning_request_query, update_learning_request_query, delete_learning_request_query, LearningRequest
from db.learning_data_query import save_learning_data_query, delete_learning_data_query, LearningData
from db.model_query import get_model_query, save_model_query, update_model_query, LearningLog, get_all_model_ids_query ,Model
import torch

async def lifespan(app: FastAPI):
    print("Starting up: creating DB pool")
    db_pool = await get_db_pool()
    app.state.db_pool = db_pool  # グローバルに保持

    yield  # ここでアプリが起動し、リクエストを処理

    print("Shutting down: closing DB pool")
    await db_pool.close()  # アプリ終了時に DB 接続を閉じる

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# モデルの生成
@app.post("/create_model")
async def create_model(request: LearningRequest):
    # パラメタを取得
    id = request.id
    name = request.name
    input_size = request.input_size
    model_orders = request.model_orders  # List[LayerOrder]
    criterion_order = request.criterion_order
    num_epochs = request.num_epochs
    batch_size = request.batch_size
    train_data_id = request.train_data_id
    test_data_id = request.test_data_id

    # DB接続を取得
    db_pool = app.state.db_pool

    # 既にモデルが存在するか確認
    selected_model = None
    async with db_pool.acquire() as conn:
        selected_model = await get_model_query(conn, id)

    # データをGETする
    total_data = 1000
    inputs = torch.randn(total_data, input_size)
    labels = torch.randint(0, 2, (total_data, 1)).float()

    # モデルを生成する
    model = generate_model(input_size, model_orders, criterion_order, num_epochs, batch_size, inputs, labels)
    
    # モデルをバイナリに変換する
    buffer = io.BytesIO()
    torch.save(model, buffer)
    model_bytea = buffer.getvalue()

    # 学習履歴の更新データを作成
    learning_history = []
    if selected_model is None:
        learning_history = [
            LearningLog(
                accuracy=0.0,
                learning_request=request
            )
        ]
    else:
        learning_history = selected_model.learning_history
        learning_history.append(
            LearningLog(
                accuracy=0.0,
                learning_request=request
            )
        )
    #print(learning_history)
    # model保存リクエストを作成
    req = Model(
        id=id,
        name=name,
        nn=model_bytea,
        learning_history=learning_history,
        created_at=request.created_at,
        updated_at=request.updated_at
    )

    # モデルを保存する
    async with db_pool.acquire() as conn:
        try:
            if selected_model is None:
                await save_model_query(conn, req)
            else:
                print("update")
                await update_model_query(conn, req)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return model #仮

# モデルのidのみ全件取得
@app.get("/get_all_model_ids")
async def get_all_model_ids():
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            model_ids = await get_all_model_ids_query(conn)
            return {"model_ids": model_ids}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# モデルの取得（1件）
@app.get("/get_model")
async def get_model(request: GetRequest):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            model = await get_model_query(conn, request.id)
            if model is None:
                raise HTTPException(status_code=404, detail="Model not found")
            return model
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# 学習リクエストの保存
@app.post("/save_learninig_request")
async def save_learninig_request(request: LearningRequest):
    pool = await get_db_pool()
    print("/save_learninig_request")
    async with pool.acquire() as conn:
        try:
            await save_learning_request_query(conn,request)
            print("sucsess")
            return {"message": "Data saved successfully"}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))

# 学習リクエストの更新
@app.put("/update_learninig_request")
async def update_learninig_request(request: LearningRequest):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            await update_learning_request_query(conn,request)
            return {"message": "Data update successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# 学習リクエストの削除
@app.delete("/delete_learninig_request")
async def delete_learninig_request(request: DeleteRequest):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            await delete_learning_request_query(conn, request.id)
            return {"message": "Data delete successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# 学習データの生成・保存
@app.post("/create_learning_data")
async def create_data(request: CreateLearningDataRequest):
    feature = request.feature
    first_text_order = request.first_text_order
    second_text_order = request.second_text_order
    option_oder = request.option_oder

    prompt = ""

    if feature is not None:
        prompt = prompt_score(feature, option_oder)
    elif first_text_order is not None and second_text_order is not None:
        prompt = prompt_relevance(first_text_order, second_text_order, option_oder)
    else:
        raise HTTPException(status_code=400, detail="リクエストのパターンが不正です")
    
    response = await get_completion(prompt)

    json_data = make_json(response)

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            await save_learning_data_query(conn, LearningData(
                id=str(uuid.uuid4()),
                name="generated_data",
                data=json_data,
            ))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return json_data #仮

# 学習データの削除
@app.delete("/delete_learning_data")
async def delete_learning_data(request: DeleteRequest):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            await delete_learning_data_query(conn, request.id)
            return {"message": "Data delete successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
