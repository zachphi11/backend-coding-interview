"""
Tests for authentication endpoints.
"""
import pytest
from fastapi import status


def test_register_user(client):
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "differentuser",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]


def test_register_duplicate_username(client, test_user):
    """Test registration with duplicate username."""
    response = client.post(
        "/auth/register",
        json={
            "email": "different@example.com",
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username already taken" in response.json()["detail"]


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpass123"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials."""
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "password123"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token(client, test_user):
    """Test token refresh."""
    # First login
    login_response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpass123"},
    )
    refresh_token = login_response.json()["refresh_token"]

    # Refresh token
    response = client.post(f"/auth/refresh?refresh_token={refresh_token}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
