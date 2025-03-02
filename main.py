from fastapi import FastAPI
from fastapi import HTTPException
from classes.model import LearningRequest
from classes.data import DataRequest
from generate_model.learning import generate_model
from generate_data.prompt import prompt_relevance, prompt_score, make_json
from generate_data.groq import get_completion
from db.save_model_request import save_learning_request_query, update_learning_request_query, delete_learning_request_query
import torch

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/create_model")
async def create_model(request: LearningRequest):
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

@app.post("/save_learninig_request")
async def save_learninig_request(request: LearningRequest):
    save_learning_request_query(request)

@app.post("/update_learninig_request")
async def update_learninig_request(request: LearningRequest):
    update_learning_request_query(request)

@app.post("/delete_learninig_request")
async def delete_learninig_request(request: LearningRequest):
    delete_learning_request_query(request)


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

