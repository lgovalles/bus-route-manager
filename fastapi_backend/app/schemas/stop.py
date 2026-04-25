from pydantic import BaseModel, ConfigDict, Field, field_validator

class StopBase(BaseModel):
    name: str = Field(..., min_length=1)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str) -> str:
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                raise ValueError("name must not be blank")
            return stripped
        return v

class StopCreate(StopBase):
    pass

class Stop(StopBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class StopInRoute(Stop):
    """Stop with order information when retrieved from a route"""
    stop_order: int = Field(..., ge=0)

    model_config = ConfigDict(from_attributes=True)