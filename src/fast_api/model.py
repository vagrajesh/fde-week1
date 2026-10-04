import pydantic

class Employee(pydantic.BaseModel):
    id: int
    name: str
    position: str