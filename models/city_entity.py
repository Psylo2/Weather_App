from typing import Optional
from pydantic import BaseModel, validator


class CityEntity(BaseModel):
    id: Optional[int]
    name: str

    @validator('name', always=True)
    def validate_str(cls, v):
        if not isinstance(v, str):
            raise TypeError("Type must be integer")
        return v
