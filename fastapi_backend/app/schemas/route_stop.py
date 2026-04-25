from pydantic import BaseModel, ConfigDict, Field

class RouteStopBase(BaseModel):
    route_id: int = Field(..., gt=0)
    stop_id: int = Field(..., gt=0)
    stop_order: int = Field(..., ge=0)

class RouteStopCreate(RouteStopBase):
    pass

class RouteStop(RouteStopBase):
    id: int

    model_config = ConfigDict(from_attributes=True)