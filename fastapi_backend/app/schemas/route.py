from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List

class RouteBase(BaseModel):
    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    color: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None

    @field_validator("name", "code", mode="before")
    @classmethod
    def strip_strings(cls, v: str) -> str:
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                raise ValueError("Field must not be blank")
            return stripped
        return v

class RouteCreate(RouteBase):
    pass

class Route(RouteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)