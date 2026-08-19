"""
Health Check Tests
=================

Tests pour l'endpoint /health.
"""

import pytest
from fastapi.testclient import TestClient
from backend.api.main import app


@pytest.fixture
def client():
    """Créer un client de test."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests pour l'endpoint /health."""
    
    def test_health_check(self, client):
        """Tester que l'endpoint /health retourne un statut OK."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"
        assert "app" in data
        assert "version" in data
        assert "timestamp" in data
    
    def test_health_check_detailed(self, client):
        """Tester que l'endpoint /health/detailed retourne des informations détaillées."""
        response = client.get("/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "dependencies" in data
        assert "postgres" in data["dependencies"]
        assert "qdrant" in data["dependencies"]


# État du module
MODULE_STATUS = "IMPLEMENTED"
