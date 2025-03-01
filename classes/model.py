from pydantic import BaseModel
from typing import List, Optional

class LayerOrder(BaseModel):
    type: str
    nodes: Optional[int] = None

class LearningRequest(BaseModel):
    id: str
    input_size: int
    model_orders: List[LayerOrder]
    criterion_order: str
    num_epochs: int
    batch_size: int
    train_data_id: str
    test_data_id: str
    created_at: str
    updated_at: str