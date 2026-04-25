import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .database import Base, engine
from .routers import route_stops, routes, stops
from .settings import load_env_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

load_env_file()


def get_cors_origins() -> list[str]:
    raw_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:5174,http://localhost:5175",
    )
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


app = FastAPI(
    title="FastAPI Backend",
    description="API para gestion de rutas y paradas de transporte publico",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(routes.router)
app.include_router(stops.router)
app.include_router(route_stops.router)


@app.get("/")
async def root():
    """Redirigir a la documentacion de la API"""
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health():
    return {"status": "ok"}
