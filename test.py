from pydantic import BaseModel
from typing import List

class A(BaseModel):
    a: str

class B(BaseModel):
    b: List[A]

class Data(BaseModel):
    c: str
    e: str
    d: B

# インスタンスの作成
data_instance = Data(
    c="value_c",
    e="value_e",
    d=B(b=[A(a="value_a1"), A(a="value_a2")])
)

# JSON に変換
json_data = data_instance.model_dump_json(indent=2)
print(json_data)
