"""Tests for domain models"""
import pytest
from app.models import Route, Stop, RouteStop


def test_create_models(db_session):
    """Test creating and querying models with relationships"""
    # Create stops
    stop1 = Stop(name="Stop A", latitude=10.0, longitude=20.0)
    stop2 = Stop(name="Stop B", latitude=11.0, longitude=21.0)
    db_session.add(stop1)
    db_session.add(stop2)
    db_session.commit()

    # Create route
    route = Route(name="Route 1", code="R1", color="blue", type="bus")
    db_session.add(route)
    db_session.commit()

    # Create route stops
    route_stop1 = RouteStop(route_id=route.id, stop_id=stop1.id, stop_order=1)
    route_stop2 = RouteStop(route_id=route.id, stop_id=stop2.id, stop_order=2)
    db_session.add(route_stop1)
    db_session.add(route_stop2)
    db_session.commit()

    # Query and validate relationships
    queried_route = db_session.query(Route).filter(Route.id == route.id).first()
    assert queried_route.name == "Route 1"
    assert queried_route.code == "R1"
    assert queried_route.color == "blue"
    assert queried_route.type == "bus"
    assert len(queried_route.route_stops) == 2

    # Check stops in order
    stops = [rs.stop.name for rs in sorted(queried_route.route_stops, key=lambda x: x.stop_order)]
    assert stops == ["Stop A", "Stop B"]

    # Check coordinates
    stop_a = next(rs.stop for rs in queried_route.route_stops if rs.stop.name == "Stop A")
    assert stop_a.latitude == 10.0
    assert stop_a.longitude == 20.0

    # Check route from stop
    queried_stop = db_session.query(Stop).filter(Stop.id == stop1.id).first()
    assert len(queried_stop.route_stops) == 1
    assert queried_stop.route_stops[0].route.name == "Route 1"