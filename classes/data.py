from pydantic import BaseModel
from typing import List, Union

class LearningRelevanceData(BaseModel):
    Q: str
    D: str
    score: float

class LearningScoreData(BaseModel):
    text: str
    score: float

class LearningDataRequest(BaseModel):
    id: str
    name: str
    data: Union[List[LearningRelevanceData], List[LearningScoreData]]
    created_at: str

class LearningDataDeleteRequest(BaseModel):
    id: str