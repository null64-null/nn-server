from pydantic import BaseModel
from typing import List, Optional

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

class LearningDeleteRequest(BaseModel):
    id: str

class LearningLog(BaseModel):
    accuracy: float
    learning_request: LearningRequest

class ModelRequest(BaseModel):
    id: str
    name: str
    nn: bytes
    learning_history: Optional[List[LearningLog]] = []
    created_at: str
    updated_at: str

class ModelDeleteRequest(BaseModel):
    id: str