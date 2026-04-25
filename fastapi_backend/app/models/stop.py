from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    route_stops = relationship("RouteStop", back_populates="stop", cascade="all, delete-orphan")
