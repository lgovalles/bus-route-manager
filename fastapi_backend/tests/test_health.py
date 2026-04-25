import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestHealthEndpoint:
    """Test suite for /health endpoint"""
    
    def test_health_returns_200(self, test_client):
        """Given backend is running, when I call /health, then I receive HTTP 200"""
        response = test_client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_ok_status(self, test_client):
        """Health endpoint should return status: 'ok'"""
        response = test_client.get("/health")
        data = response.json()
        assert data["status"] == "ok"
    
    def test_health_response_is_json(self, test_client):
        """Health endpoint should return JSON content-type"""
        response = test_client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_response_structure(self, test_client):
        """Health endpoint response should have required fields"""
        response = test_client.get("/health")
        data = response.json()
        assert isinstance(data, dict)
        assert "status" in data
        assert isinstance(data["status"], str)


class TestRootEndpoint:
    """Test suite for root endpoint"""
    
    def test_root_redirects_to_docs(self, test_client):
        """Root endpoint should redirect to /docs"""
        response = test_client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/docs"
