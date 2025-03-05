from pydantic import BaseModel
from typing import List, Union, Optional

class CreateLearningDataRequest(BaseModel):
	feature: Optional[str] = None
	first_text_order: Optional[str] = None
	second_text_order: Optional[str] = None
	option_oder: Optional[str] = None

class DeleteRequest(BaseModel):
    id: str