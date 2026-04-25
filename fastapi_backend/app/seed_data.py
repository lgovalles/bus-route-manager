from sqlalchemy.orm import Session

from app.models import Route, Stop, RouteStop

STOPS_DATA = {
    "Cuatro Esquinas": {"latitude": 6.1718, "longitude": -75.3715},
    "El Rosal": {"latitude": 6.1602, "longitude": -75.3628},
    "Bodega": {"latitude": 6.1643, "longitude": -75.3862},
    "La Feria": {"latitude": 6.1528, "longitude": -75.3725},
    "Porvenir": {"latitude": 6.1492, "longitude": -75.3689},
    "San Antonio": {"latitude": 6.1165, "longitude": -75.3385},
    "Colegios": {"latitude": 6.1468, "longitude": -75.3764},
    "Aeropuerto": {"latitude": 6.16722, "longitude": -75.42667},
    "Tablazo": {"latitude": 6.1544, "longitude": -75.4102},
    "Pantanillo": {"latitude": 6.1406, "longitude": -75.3988},
    "Tanque": {"latitude": 6.1627, "longitude": -75.3658},
    "GEM": {"latitude": 6.1589, "longitude": -75.3908},
    "Llanogrande": {"latitude": 6.1298, "longitude": -75.4125},
    "Cabeceras": {"latitude": 6.1225, "longitude": -75.4034},
    "Cuchillas": {"latitude": 6.1886, "longitude": -75.3564},
    "Tránsito": {"latitude": 6.1569, "longitude": -75.3744},
    "Vilachuaga": {"latitude": 6.1449, "longitude": -75.3571},
    "Belén": {"latitude": 6.1580, "longitude": -75.3795},
    "Centro": {"latitude": 6.1550, "longitude": -75.3800},
}

ROUTES_DATA = [
    {
        "code": "01",
        "name": "Route 01 - Cuatro Esquinas - El Rosal",
        "color": "#2E86DE",
        "type": "trunk",
        "stops": ["Cuatro Esquinas", "Belén", "Centro", "El Rosal"],
    },
    {
        "code": "02",
        "name": "Route 02 - Bodega - La Feria",
        "color": "#E67E22",
        "type": "trunk",
        "stops": ["Bodega", "Belén", "Centro", "La Feria"],
    },
    {
        "code": "03",
        "name": "Route 03 - Porvenir",
        "color": "#27AE60",
        "type": "feeder",
        "stops": ["Porvenir", "Belén", "Centro"],
    },
    {
        "code": "04",
        "name": "Route 04 - San Antonio - Colegios",
        "color": "#8E44AD",
        "type": "trunk",
        "stops": ["San Antonio", "Belén", "Centro", "Colegios"],
    },
    {
        "code": "05",
        "name": "Route 05 - Aeropuerto - Tablazo - Pantanillo",
        "color": "#C0392B",
        "type": "trunk",
        "stops": ["Aeropuerto", "Tablazo", "Belén", "Centro", "Pantanillo"],
    },
    {
        "code": "06",
        "name": "Route 06 - Tanque - Centro",
        "color": "#16A085",
        "type": "feeder",
        "stops": ["Tanque", "Belén", "Centro"],
    },
    {
        "code": "07",
        "name": "Route 07 - GEM - Tablazo",
        "color": "#D35400",
        "type": "feeder",
        "stops": ["GEM", "Belén", "Centro", "Tablazo"],
    },
    {
        "code": "08",
        "name": "Route 08 - Llanogrande - Cabeceras",
        "color": "#2980B9",
        "type": "trunk",
        "stops": ["Llanogrande", "Belén", "Centro", "Cabeceras"],
    },
    {
        "code": "09",
        "name": "Route 09 - Cuchillas - Tránsito",
        "color": "#7F8C8D",
        "type": "feeder",
        "stops": ["Cuchillas", "Belén", "Centro", "Tránsito"],
    },
    {
        "code": "10",
        "name": "Route 10 - San Antonio - Vilachuaga",
        "color": "#F1C40F",
        "type": "trunk",
        "stops": ["San Antonio", "Belén", "Centro", "Vilachuaga"],
    },
]


def get_or_create_stop(db: Session, stop_name: str, latitude: float, longitude: float) -> Stop:
    stop = db.query(Stop).filter(Stop.name == stop_name).first()
    if stop:
        updated = False
        if getattr(stop, "latitude", None) != latitude:
            stop.latitude = latitude
            updated = True
        if getattr(stop, "longitude", None) != longitude:
            stop.longitude = longitude
            updated = True
        if updated:
            db.flush()
        return stop

    stop = Stop(
        name=stop_name,
        latitude=latitude,
        longitude=longitude,
    )
    db.add(stop)
    db.flush()
    return stop


def get_or_create_route(
    db: Session,
    name: str,
    code: str,
    color: str,
    type: str,
) -> Route:
    # For now, just create without checking existing
    route = Route(
        name=name,
        code=code,
        color=color,
        type=type,
    )
    db.add(route)
    db.flush()
    return route


def route_stop_exists(db: Session, route_id: int, stop_id: int, order: int) -> bool:
    return (
        db.query(RouteStop)
        .filter(
            RouteStop.route_id == route_id,
            RouteStop.stop_id == stop_id,
            RouteStop.stop_order == order,
        )
        .first()
        is not None
    )


def seed_routes_and_stops(db: Session) -> None:
    for route_data in ROUTES_DATA:
        route = get_or_create_route(
            db=db,
            name=route_data["name"],
            code=route_data["code"],
            color=route_data["color"],
            type=route_data["type"],
        )

        for index, stop_name in enumerate(route_data["stops"], start=1):
            coords = STOPS_DATA[stop_name]
            stop = get_or_create_stop(
                db=db,
                stop_name=stop_name,
                latitude=coords["latitude"],
                longitude=coords["longitude"],
            )

            if not route_stop_exists(db, route.id, stop.id, index):
                db.add(
                    RouteStop(
                        route_id=route.id,
                        stop_id=stop.id,
                        stop_order=index,
                    )
                )

    db.commit()


def seed_database(db: Session) -> None:
    seed_routes_and_stops(db)


if __name__ == "__main__":
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        seed_database(db)
        print("Seed completed successfully.")
    except Exception as exc:
        db.rollback()
        print(f"Seed failed: {exc}")
        raise
    finally:
        db.close()
