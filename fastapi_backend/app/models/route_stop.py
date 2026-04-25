from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from ..database import Base


class RouteStop(Base):
    __tablename__ = "route_stops"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    stop_id = Column(Integer, ForeignKey("stops.id"), nullable=False)
    stop_order = Column(Integer, nullable=False)

    route = relationship("Route", back_populates="route_stops")
    stop = relationship("Stop", back_populates="route_stops")

    __table_args__ = (
        # A stop can only appear once per route
        UniqueConstraint("route_id", "stop_id", name="uq_route_stop"),
        # A route can only have one stop at each position
        UniqueConstraint("route_id", "stop_order", name="uq_route_order"),
    )
