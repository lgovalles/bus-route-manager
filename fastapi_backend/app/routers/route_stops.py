import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..dependencies import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/route-stops", tags=["route-stops"])


@router.post("/", response_model=schemas.RouteStop)
def create_route_stop(route_stop: schemas.RouteStopCreate, db: Session = Depends(get_db)):
    # Check if route and stop exist
    db_route = db.query(models.Route).filter(models.Route.id == route_stop.route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    db_stop = db.query(models.Stop).filter(models.Stop.id == route_stop.stop_id).first()
    if not db_stop:
        raise HTTPException(status_code=404, detail="Stop not found")

    # Check for duplicate route-stop
    existing = (
        db.query(models.RouteStop)
        .filter(
            models.RouteStop.route_id == route_stop.route_id,
            models.RouteStop.stop_id == route_stop.stop_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Duplicate or invalid route-stop")

    db_route_stop = models.RouteStop(**route_stop.model_dump())
    db.add(db_route_stop)
    try:
        db.commit()
        db.refresh(db_route_stop)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate or invalid route-stop") from None
    return db_route_stop


@router.get("/", response_model=list[schemas.RouteStop])
def read_route_stops(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    route_stops = db.query(models.RouteStop).offset(skip).limit(limit).all()
    return route_stops


@router.get("/{route_stop_id}", response_model=schemas.RouteStop)
def read_route_stop(route_stop_id: int, db: Session = Depends(get_db)):
    db_route_stop = db.query(models.RouteStop).filter(models.RouteStop.id == route_stop_id).first()
    if db_route_stop is None:
        raise HTTPException(status_code=404, detail="RouteStop not found")
    return db_route_stop


@router.put("/{route_stop_id}", response_model=schemas.RouteStop)
def update_route_stop(
    route_stop_id: int, route_stop: schemas.RouteStopCreate, db: Session = Depends(get_db)
):
    db_route_stop = db.query(models.RouteStop).filter(models.RouteStop.id == route_stop_id).first()
    if db_route_stop is None:
        raise HTTPException(status_code=404, detail="RouteStop not found")
    for key, value in route_stop.model_dump().items():
        setattr(db_route_stop, key, value)
    try:
        db.commit()
        db.refresh(db_route_stop)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed") from None
    return db_route_stop


@router.delete("/{route_stop_id}")
def delete_route_stop(route_stop_id: int, db: Session = Depends(get_db)):
    db_route_stop = db.query(models.RouteStop).filter(models.RouteStop.id == route_stop_id).first()
    if db_route_stop is None:
        raise HTTPException(status_code=404, detail="RouteStop not found")
    db.delete(db_route_stop)
    db.commit()
    logger.info("Deleted route_stop id=%s", route_stop_id)
    return {"message": "RouteStop deleted"}
