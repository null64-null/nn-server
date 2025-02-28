from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
from generate_model.learning import generate_model
from generate_data.prompt import prompt_relevance, prompt_score, make_json
from generate_data.groq import get_completion
import torch

app = FastAPI()

class LayerOrder(BaseModel):
    type: str
    nodes: Optional[int] = None

class ModelRequest(BaseModel):
    input_size: int
    model_orders: List[LayerOrder]
    criterion_order: str
    num_epochs: int
    batch_size: int
    #inputs: List[List[float]]
    #labels: List[float]

class DataRequest(BaseModel):
    feature: Optional[str] = None
    first_text_order: Optional[str] = None
    second_text_order: Optional[str] = None
    option_oder: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/create_model")
async def create_model(request: ModelRequest):
    input_size = request.input_size
    model_orders = request.model_orders  # List[LayerOrder]
    criterion_order = request.criterion_order
    num_epochs = request.num_epochs
    batch_size = request.batch_size

    #inputs = request.inputs  # List[List[float]]
    #labels = request.labels  # List[float]
    total_data = 1000
    inputs = torch.randn(total_data, input_size)
    labels = torch.randint(0, 2, (total_data, 1)).float()

    print(inputs)
    print(labels)

    state_dict = generate_model(input_size, model_orders, criterion_order, num_epochs, batch_size, inputs, labels)
    return state_dict

@app.post("/create_data")
async def create_data(request: DataRequest):
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
    
    return json_data