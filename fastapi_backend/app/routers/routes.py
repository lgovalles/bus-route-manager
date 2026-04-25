import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..dependencies import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/routes", tags=["routes"])

@router.post("/", response_model=schemas.Route)
def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    db_route = models.Route(**route.model_dump())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

@router.get("/", response_model=List[schemas.Route])
def read_routes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    routes = db.query(models.Route).offset(skip).limit(limit).all()
    return routes

@router.get("/{route_id}", response_model=schemas.Route)
def read_route(route_id: int, db: Session = Depends(get_db)):
    db_route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route

@router.get("/{route_id}/stops", response_model=List[schemas.StopInRoute])
def get_route_stops(route_id: int, db: Session = Depends(get_db)):
    """
    Get all stops for a route in order.
    
    Returns stops with their order information sorted by stop_order.
    """
    # Verify route exists
    db_route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Query route_stops ordered by stop_order and fetch associated stops
    route_stops = (
        db.query(models.RouteStop, models.Stop)
        .filter(models.RouteStop.route_id == route_id)
        .join(models.Stop, models.RouteStop.stop_id == models.Stop.id)
        .order_by(models.RouteStop.stop_order)
        .all()
    )
    
    # Transform the results to match StopInRoute schema
    result = []
    for route_stop, stop in route_stops:
        stop_in_route = {
            "id": stop.id,
            "name": stop.name,
            "latitude": stop.latitude,
            "longitude": stop.longitude,
            "stop_order": route_stop.stop_order
        }
        result.append(stop_in_route)
    
    return result

@router.put("/{route_id}", response_model=schemas.Route)
def update_route(route_id: int, route: schemas.RouteCreate, db: Session = Depends(get_db)):
    db_route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    for key, value in route.model_dump().items():
        setattr(db_route, key, value)
    db.commit()
    db.refresh(db_route)
    return db_route

@router.delete("/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db)):
    db_route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    logger.info("Deleting route id=%s", route_id)
    db.delete(db_route)
    db.commit()
    return {"message": "Route deleted"}