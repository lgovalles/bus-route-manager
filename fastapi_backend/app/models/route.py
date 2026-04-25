from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    code = Column(String, nullable=False)
    color = Column(String)
    description = Column(String)
    type = Column(String)
    # route_type = Column(String)

    route_stops = relationship("RouteStop", back_populates="route", cascade="all, delete-orphan")
