from pydantic import BaseModel


class ProductIn(BaseModel):
    name: str


class ProductOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
