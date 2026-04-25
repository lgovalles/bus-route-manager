# FastAPI Backend

## Setup

1. cd C:\\Users\\lovalles\\fastapi_backend
2. python -m venv venv
3. .\\venv\\Scripts\\Activate.ps1
4. pip install --upgrade pip
5. pip install -r requirements.txt
6. pip install -r requirements-dev.txt
7. Optionally create a `.env` file from `.env.example`

## Environment Variables

```bash
DATABASE_URL=sqlite:///./app.db
CORS_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:5175
```

## Run

```bash
uvicorn app.main:app --reload
```

**Accede a la API:**
- **Documentación interactiva**: http://127.0.0.1:8000 (redirecciona automáticamente a /docs)
- **Health check**: http://127.0.0.1:8000/health

Si no defines variables de entorno, el backend usa esos valores por defecto en desarrollo.

## Unit Tests

```bash
python -m pytest tests/ -v
```

## Quality and Security Checks

```bash
ruff check .
ruff format --check .
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
bandit -q -r app -x tests
pip-audit -r requirements.txt
```

All tests should pass (46/46).

### Test Structure

```
tests/
  ├── __init__.py           # Package marker
  ├── conftest.py           # Pytest configuration & fixtures
  ├── test_endpoints.py     # API endpoint tests (40 tests including edge cases)
  ├── test_health.py        # Health endpoint tests
  └── test_models.py        # Model and relationship tests
```

### Test Coverage

Current test coverage: **83%**

The test suite includes comprehensive edge case testing:
- 404 error scenarios for all endpoints
- Input validation tests
- Negative scenarios (duplicates, invalid data, wrong content types)

## API Endpoints

### Stops
- `POST /stops/` - Create a stop
- `GET /stops/` - List stops
- `GET /stops/{stop_id}` - Get stop by ID
- `PUT /stops/{stop_id}` - Update stop
- `DELETE /stops/{stop_id}` - Delete stop

### Routes
- `POST /routes/` - Create a route
- `GET /routes/` - List routes
- `GET /routes/{route_id}` - Get route by ID
- `PUT /routes/{route_id}` - Update route
- `DELETE /routes/{route_id}` - Delete route

### Route-Stops
- `POST /route-stops/` - Create a route-stop association
- `GET /route-stops/` - List route-stops
- `GET /route-stops/{route_stop_id}` - Get route-stop by ID
- `PUT /route-stops/{route_stop_id}` - Update route-stop
- `DELETE /route-stops/{route_stop_id}` - Delete route-stop
