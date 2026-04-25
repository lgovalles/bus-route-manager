import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..dependencies import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/stops", tags=["stops"])


@router.post("/", response_model=schemas.Stop)
def create_stop(stop: schemas.StopCreate, db: Session = Depends(get_db)):
    db_stop = models.Stop(**stop.model_dump())
    db.add(db_stop)
    db.commit()
    db.refresh(db_stop)
    return db_stop


@router.get("/", response_model=list[schemas.Stop])
def read_stops(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    GET /paraderos - Load Sonrío routes data

    Retrieve all stops (paraderos) for the transportation system.

    Returns a list of all stops with their geographic coordinates.
    Supports pagination with skip and limit parameters.

    **Acceptance Criteria:**
    - Given DB is initialized
    - When routes are queried
    - Then data exists

    **Definition of Done:**
    - Realistic data available (Belén, Airport, etc.)
    - Routes 01-10 minimum inserted
    - Key stops Belén, Airport, etc. inserted
    - Data validated

    Query Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum records to return (default: 100)

    Returns:
    - List[Stop]: Array of stops with id, name, latitude, longitude
    """
    stops = db.query(models.Stop).offset(skip).limit(limit).all()
    return stops


@router.get("/{stop_id}", response_model=schemas.Stop)
def read_stop(stop_id: int, db: Session = Depends(get_db)):
    db_stop = db.query(models.Stop).filter(models.Stop.id == stop_id).first()
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return db_stop


@router.put("/{stop_id}", response_model=schemas.Stop)
def update_stop(stop_id: int, stop: schemas.StopCreate, db: Session = Depends(get_db)):
    db_stop = db.query(models.Stop).filter(models.Stop.id == stop_id).first()
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    for key, value in stop.model_dump().items():
        setattr(db_stop, key, value)
    db.commit()
    db.refresh(db_stop)
    return db_stop


@router.delete("/{stop_id}")
def delete_stop(stop_id: int, db: Session = Depends(get_db)):
    db_stop = db.query(models.Stop).filter(models.Stop.id == stop_id).first()
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    db.delete(db_stop)
    db.commit()
    logger.info("Deleted stop id=%s", stop_id)
    return {"message": "Stop deleted"}
