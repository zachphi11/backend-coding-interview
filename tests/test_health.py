"""
Tests for health check endpoints.
"""
from fastapi import status


def test_health_check(client):
    """Test basic health check."""
    response = client.get("/health/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"


def test_database_health_check(client):
    """Test database health check."""
    response = client.get("/health/db")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
