from pydantic import BaseModel, ConfigDict, Field, field_validator


class RouteBase(BaseModel):
    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    color: str | None = None
    description: str | None = None
    type: str | None = None

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
