"""Tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Remove global client, use fixture instead

def test_create_stop(test_client):
    response = test_client.post("/stops/", json={"name": "Test Stop", "latitude": 10.0, "longitude": 20.0})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Stop"
    assert data["latitude"] == 10.0

def test_create_route(test_client):
    response = test_client.post("/routes/", json={"name": "Test Route", "code": "TR1", "color": "red", "type": "bus"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Route"
    assert data["code"] == "TR1"

def test_read_stops(test_client):
    response = test_client.get("/stops/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_routes(test_client):
    response = test_client.get("/routes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Tests for GET /routes/{route_id}/stops endpoint
def test_get_route_stops(test_client):
    """Test retrieving stops for a route - happy path"""
    # Create a route
    route_response = test_client.post("/routes/", json={"name": "Test Route", "code": "TR1"})
    route_id = route_response.json()["id"]
    
    # Create stops
    stop1 = test_client.post("/stops/", json={"name": "Stop 1", "latitude": 10.0, "longitude": 20.0}).json()
    stop2 = test_client.post("/stops/", json={"name": "Stop 2", "latitude": 15.0, "longitude": 25.0}).json()
    stop3 = test_client.post("/stops/", json={"name": "Stop 3", "latitude": 20.0, "longitude": 30.0}).json()
    
    # Create route-stops with specific order
    test_client.post("/route-stops/", json={"route_id": route_id, "stop_id": stop1["id"], "stop_order": 0})
    test_client.post("/route-stops/", json={"route_id": route_id, "stop_id": stop3["id"], "stop_order": 2})
    test_client.post("/route-stops/", json={"route_id": route_id, "stop_id": stop2["id"], "stop_order": 1})
    
    # Get route stops
    response = test_client.get(f"/routes/{route_id}/stops")
    assert response.status_code == 200
    data = response.json()
    
    # Verify correct number of stops
    assert len(data) == 3
    
    # Verify stops are ordered by stop_order
    assert data[0]["stop_order"] == 0
    assert data[0]["name"] == "Stop 1"
    assert data[0]["latitude"] == 10.0
    assert data[0]["longitude"] == 20.0
    
    assert data[1]["stop_order"] == 1
    assert data[1]["name"] == "Stop 2"
    
    assert data[2]["stop_order"] == 2
    assert data[2]["name"] == "Stop 3"
    
    # Verify all fields are present
    for stop in data:
        assert "id" in stop
        assert "name" in stop
        assert "latitude" in stop
        assert "longitude" in stop
        assert "stop_order" in stop


def test_get_route_stops_empty(test_client):
    """Test retrieving stops for a route with no stops"""
    # Create a route
    route_response = test_client.post("/routes/", json={"name": "Empty Route", "code": "ER1"})
    route_id = route_response.json()["id"]
    
    # Get route stops
    response = test_client.get(f"/routes/{route_id}/stops")
    assert response.status_code == 200
    assert response.json() == []


def test_get_route_stops_not_found(test_client):
    """Test retrieving stops for a non-existent route"""
    response = test_client.get("/routes/999/stops")
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"


# 404 Cases - Stops
def test_get_stop_not_found(test_client):
    response = test_client.get("/stops/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Stop not found"

def test_update_stop_not_found(test_client):
    response = test_client.put("/stops/999", json={"name": "Updated Stop", "latitude": 15.0, "longitude": 25.0})
    assert response.status_code == 404
    assert response.json()["detail"] == "Stop not found"

def test_delete_stop_not_found(test_client):
    response = test_client.delete("/stops/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Stop not found"


# 404 Cases - Routes
def test_get_route_not_found(test_client):
    response = test_client.get("/routes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"

def test_update_route_not_found(test_client):
    response = test_client.put("/routes/999", json={"name": "Updated Route", "code": "UR1", "color": "blue", "type": "train"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"

def test_delete_route_not_found(test_client):
    response = test_client.delete("/routes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"


# 404 Cases - Route-Stops
def test_get_route_stop_not_found(test_client):
    response = test_client.get("/route-stops/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "RouteStop not found"

def test_update_route_stop_not_found(test_client):
    response = test_client.put("/route-stops/999", json={"route_id": 1, "stop_id": 1, "stop_order": 1})
    assert response.status_code == 404
    assert response.json()["detail"] == "RouteStop not found"

def test_delete_route_stop_not_found(test_client):
    response = test_client.delete("/route-stops/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "RouteStop not found"

def test_create_route_stop_invalid_route(test_client):
    response = test_client.post("/route-stops/", json={"route_id": 999, "stop_id": 1, "stop_order": 1})
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"

def test_create_route_stop_invalid_stop(test_client):
    # Create a route first
    test_client.post("/routes/", json={"name": "Test Route", "code": "TR1"})
    response = test_client.post("/route-stops/", json={"route_id": 1, "stop_id": 999, "stop_order": 1})
    assert response.status_code == 404
    assert response.json()["detail"] == "Stop not found"


# Validation Tests - Stops
def test_create_stop_missing_name(test_client):
    response = test_client.post("/stops/", json={"latitude": 10.0, "longitude": 20.0})
    assert response.status_code == 422  # Validation error

def test_create_stop_missing_latitude(test_client):
    response = test_client.post("/stops/", json={"name": "Test Stop", "longitude": 20.0})
    assert response.status_code == 422

def test_create_stop_invalid_latitude_type(test_client):
    response = test_client.post("/stops/", json={"name": "Test Stop", "latitude": "invalid", "longitude": 20.0})
    assert response.status_code == 422

def test_create_stop_invalid_latitude_range(test_client):
    response = test_client.post("/stops/", json={"name": "Test Stop", "latitude": 100.0, "longitude": 20.0})
    assert response.status_code == 422

def test_create_stop_invalid_longitude_range(test_client):
    response = test_client.post("/stops/", json={"name": "Test Stop", "latitude": 10.0, "longitude": 200.0})
    assert response.status_code == 422


# Validation Tests - Routes
def test_create_route_missing_name(test_client):
    response = test_client.post("/routes/", json={"code": "TR1", "color": "red", "type": "bus"})
    assert response.status_code == 422

def test_create_route_missing_code(test_client):
    response = test_client.post("/routes/", json={"name": "Test Route", "color": "red", "type": "bus"})
    assert response.status_code == 422

def test_create_route_invalid_name_type(test_client):
    response = test_client.post("/routes/", json={"name": 123, "code": "TR1", "color": "red", "type": "bus"})
    assert response.status_code == 422


# Validation Tests - Route-Stops
def test_create_route_stop_missing_route_id(test_client):
    response = test_client.post("/route-stops/", json={"stop_id": 1, "stop_order": 1})
    assert response.status_code == 422

def test_create_route_stop_missing_stop_id(test_client):
    response = test_client.post("/route-stops/", json={"route_id": 1, "stop_order": 1})
    assert response.status_code == 422

def test_create_route_stop_missing_stop_order(test_client):
    response = test_client.post("/route-stops/", json={"route_id": 1, "stop_id": 1})
    assert response.status_code == 422

def test_create_route_stop_invalid_stop_order(test_client):
    response = test_client.post("/route-stops/", json={"route_id": 1, "stop_id": 1, "stop_order": -1})
    assert response.status_code == 422


# Negative Scenarios
def test_create_route_stop_duplicate(test_client):
    # First create a route and stop
    test_client.post("/routes/", json={"name": "Test Route", "code": "TR1"})
    test_client.post("/stops/", json={"name": "Test Stop", "latitude": 10.0, "longitude": 20.0})
    
    # Create route-stop
    response = test_client.post("/route-stops/", json={"route_id": 1, "stop_id": 1, "stop_order": 1})
    assert response.status_code == 200
    
    # Try to create the same one again
    response = test_client.post("/route-stops/", json={"route_id": 1, "stop_id": 1, "stop_order": 1})
    assert response.status_code == 400
    assert "Duplicate or invalid route-stop" in response.json()["detail"]

def test_invalid_json_payload(test_client):
    response = test_client.post("/stops/", data="invalid json")
    assert response.status_code == 422

def test_wrong_content_type(test_client):
    response = test_client.post("/stops/", data="name=Test&latitude=10.0&longitude=20.0", 
                          headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 422


# ============================================================================
# ACCEPTANCE CRITERIA: GET /paraderos - Load Sonrío routes data
# Given DB is initialized
# When routes are queried
# Then data exists
# ============================================================================

def test_get_paraderos_returns_stops(test_client):
    """AC: Given DB is initialized, When routes are queried, Then data exists"""
    # Create test stops with realistic data
    stops_to_create = [
        {"name": "Belén", "latitude": 9.9281, "longitude": -84.6783},
        {"name": "Aeropuerto Juan Manuel Fernández", "latitude": 10.5926, "longitude": -85.2617},
        {"name": "San José Centro", "latitude": 9.9281, "longitude": -84.0750},
    ]
    
    for stop in stops_to_create:
        test_client.post("/stops/", json=stop)
    
    # Query GET /stops (paraderos endpoint)
    response = test_client.get("/stops/")
    assert response.status_code == 200
    data = response.json()
    
    # Then data exists
    assert len(data) == 3
    assert isinstance(data, list)


def test_paraderos_contains_key_stops(test_client):
    """DoD: Realistic data available - Key stops (Belén, Airport, etc.)"""
    # Insert key stops
    key_stops = [
        {"name": "Belén", "latitude": 9.9281, "longitude": -84.6783},
        {"name": "Aeropuerto Juan Manuel Fernández", "latitude": 10.5926, "longitude": -85.2617},
    ]
    
    for stop in key_stops:
        test_client.post("/stops/", json=stop)
    
    # Verify they exist in GET /stops
    response = test_client.get("/stops/")
    assert response.status_code == 200
    data = response.json()
    
    stop_names = [s["name"] for s in data]
    assert "Belén" in stop_names
    assert "Aeropuerto Juan Manuel Fernández" in stop_names


def test_routes_minimum_10_routes(test_client):
    """Checklist: Insert routes (01–10 minimum)"""
    # Create 10 routes with codes 01-10
    routes = [
        {"code": f"{i:02d}", "name": f"Ruta {i:02d}", "color": "red", "type": "bus"}
        for i in range(1, 11)
    ]
    
    for route in routes:
        test_client.post("/routes/", json=route)
    
    # Verify all routes exist
    response = test_client.get("/routes/")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 10
    route_codes = [r["code"] for r in data]
    
    for i in range(1, 11):
        assert f"{i:02d}" in route_codes


def test_paraderos_data_validation(test_client):
    """Validate data - stops have required fields"""
    stop_data = {
        "name": "Test Stop",
        "latitude": 9.9281,
        "longitude": -84.6783
    }
    
    response = test_client.post("/stops/", json=stop_data)
    assert response.status_code == 200
    
    created_stop = response.json()
    
    # Validate all required fields are present
    assert "id" in created_stop
    assert "name" in created_stop
    assert "latitude" in created_stop
    assert "longitude" in created_stop
    
    # Validate data is correct
    assert created_stop["name"] == "Test Stop"
    assert created_stop["latitude"] == 9.9281
    assert created_stop["longitude"] == -84.6783


def test_paraderos_coordinates_realistic(test_client):
    """DoD: Realistic data available - coordinates within Costa Rica"""
    # Create stops with realistic Costa Rica coordinates
    stops = [
        {"name": "Belén", "latitude": 9.9281, "longitude": -84.6783},
        {"name": "Aeropuerto", "latitude": 10.5926, "longitude": -85.2617},
    ]
    
    for stop in stops:
        response = test_client.post("/stops/", json=stop)
        data = response.json()
        
        # Costa Rica latitude: 8° N to 11° N
        # Costa Rica longitude: 82° W to 86° W
        assert 8 <= data["latitude"] <= 11
        assert -86 <= data["longitude"] <= -82


def test_get_paraderos_with_seed_data(db_with_seed_data):
    """
    INTEGRATION TEST: Verify complete implementation
    
    Given DB is initialized with seed data
    When GET /paraderos is queried
    Then all realistic data exists
    """
    response = db_with_seed_data.get("/stops/")
    assert response.status_code == 200
    
    stops = response.json()
    
    # Verify realistic data loaded
    assert len(stops) >= 14  # At least initial stops
    
    # Verify key stops exist
    stop_names = [s["name"] for s in stops]
    assert "Belén" in stop_names
    assert "Aeropuerto" in stop_names
    
    # Verify all stops have required fields
    for stop in stops:
        assert "id" in stop
        assert "name" in stop
        assert "latitude" in stop
        assert "longitude" in stop
        
        # Verify coordinates are valid
        assert isinstance(stop["latitude"], float)
        assert isinstance(stop["longitude"], float)
        assert -180 <= stop["longitude"] <= 180
        assert -90 <= stop["latitude"] <= 90


def test_get_routes_with_seed_data(db_with_seed_data):
    """
    INTEGRATION TEST: Verify routes are initialized
    
    Checklist: Insert routes (01–10 minimum)
    """
    response = db_with_seed_data.get("/routes/")
    assert response.status_code == 200
    
    routes = response.json()
    
    # Verify minimum 10 routes
    assert len(routes) >= 10
    
    # Verify route codes 01-10 exist
    route_codes = [r["code"] for r in routes]
    for i in range(1, 11):
        assert f"{i:02d}" in route_codes
    
    # Verify all routes have required fields
    for route in routes:
        assert "id" in route
        assert "name" in route
        assert "code" in route
        assert "color" in route or "type" in route


# ============================================================================
# Successful DELETE operations (regression for missing db.commit bug)
# ============================================================================

def test_delete_route_success(test_client):
    """Verify a route is actually removed after DELETE"""
    response = test_client.post("/routes/", json={"name": "To Delete", "code": "DEL1"})
    assert response.status_code == 200
    route_id = response.json()["id"]

    delete_response = test_client.delete(f"/routes/{route_id}")
    assert delete_response.status_code == 200

    # Route must no longer exist
    get_response = test_client.get(f"/routes/{route_id}")
    assert get_response.status_code == 404


def test_delete_stop_success(test_client):
    """Verify a stop is actually removed after DELETE"""
    response = test_client.post("/stops/", json={"name": "To Delete", "latitude": 9.9, "longitude": -84.1})
    assert response.status_code == 200
    stop_id = response.json()["id"]

    delete_response = test_client.delete(f"/stops/{stop_id}")
    assert delete_response.status_code == 200

    get_response = test_client.get(f"/stops/{stop_id}")
    assert get_response.status_code == 404


def test_delete_route_stop_success(test_client):
    """Verify a route-stop association is actually removed after DELETE"""
    route_id = test_client.post("/routes/", json={"name": "R1", "code": "R1"}).json()["id"]
    stop_id = test_client.post("/stops/", json={"name": "S1", "latitude": 9.9, "longitude": -84.1}).json()["id"]
    rs_id = test_client.post(
        "/route-stops/", json={"route_id": route_id, "stop_id": stop_id, "stop_order": 0}
    ).json()["id"]

    delete_response = test_client.delete(f"/route-stops/{rs_id}")
    assert delete_response.status_code == 200

    get_response = test_client.get(f"/route-stops/{rs_id}")
    assert get_response.status_code == 404


# ============================================================================
# Pagination validation
# ============================================================================

def test_pagination_invalid_skip_negative(test_client):
    """Negative skip should be rejected with 422"""
    assert test_client.get("/routes/?skip=-1").status_code == 422
    assert test_client.get("/stops/?skip=-1").status_code == 422
    assert test_client.get("/route-stops/?skip=-1").status_code == 422


def test_pagination_invalid_limit_zero(test_client):
    """Limit=0 should be rejected"""
    assert test_client.get("/routes/?limit=0").status_code == 422
    assert test_client.get("/stops/?limit=0").status_code == 422


def test_pagination_invalid_limit_too_large(test_client):
    """Limit > 1000 should be rejected"""
    assert test_client.get("/routes/?limit=1001").status_code == 422
    assert test_client.get("/stops/?limit=1001").status_code == 422


# ============================================================================
# Field validator — whitespace stripping
# ============================================================================

def test_create_stop_strips_whitespace(test_client):
    """Names with surrounding whitespace should be stored trimmed"""
    response = test_client.post("/stops/", json={"name": "  Belén  ", "latitude": 9.9, "longitude": -84.1})
    assert response.status_code == 200
    assert response.json()["name"] == "Belén"


def test_create_route_strips_whitespace(test_client):
    """Route name and code should be trimmed"""
    response = test_client.post("/routes/", json={"name": "  Ruta 01  ", "code": " 01 "})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ruta 01"
    assert data["code"] == "01"


def test_create_stop_blank_name_rejected(test_client):
    """Blank name (only whitespace) must be rejected"""
    response = test_client.post("/stops/", json={"name": "   ", "latitude": 9.9, "longitude": -84.1})
    assert response.status_code == 422