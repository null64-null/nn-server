from pydantic import BaseModel
from typing import List, Optional

class LayerOrder(BaseModel):
    type: str
    nodes: Optional[int] = None

class ModelRequest(BaseModel):
    input_size: int
    model_orders: List[LayerOrder]
    criterion_order: str
    num_epochs: int
    batch_size: int