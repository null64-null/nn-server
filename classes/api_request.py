from pydantic import BaseModel
from typing import List, Union, Optional

class CreateLearningDataRequest(BaseModel):
    id: str
    name: str
    discription: Optional[str] = None
    text_length: int
    data_length: int
    feature: Optional[str] = None
    first_text_order: Optional[str] = None
    second_text_order: Optional[str] = None
    option_order: Optional[str] = None
    

class DeleteRequest(BaseModel):
    id: str

class GetRequest(BaseModel):
    id: str
    
class InferenceRequest(BaseModel):
    text: str
    tokens_length: int
    model_id: str