from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from generate_model.learning import generate_model
import torch

app = FastAPI()

class LayerOrder(BaseModel):
    type: str
    nodes: Optional[int] = None  # "Linear" のときだけ "nodes" が必要

class ModelRequest(BaseModel):
    input_size: int
    model_orders: List[LayerOrder]
    criterion_order: str
    num_epochs: int
    batch_size: int
    #inputs: List[List[float]]
    #labels: List[float]


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
