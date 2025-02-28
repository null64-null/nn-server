from pydantic import BaseModel
from typing import Optional
class DataRequest(BaseModel):
    feature: Optional[str] = None
    first_text_order: Optional[str] = None
    second_text_order: Optional[str] = None
    option_oder: Optional[str] = None