"""
Tests for photo endpoints.
"""
import pytest
from fastapi import status
from app.models.photo import Photo


@pytest.fixture
def test_photo(db):
    """Create a test photo."""
    photo = Photo(
        id=1,
        width=1920,
        height=1080,
        url="https://example.com/photo",
        photographer="Test Photographer",
        photographer_url="https://example.com/photographer",
        photographer_id=123,
        avg_color="#FFFFFF",
        src_original="https://example.com/original.jpg",
        src_large2x="https://example.com/large2x.jpg",
        src_large="https://example.com/large.jpg",
        src_medium="https://example.com/medium.jpg",
        src_small="https://example.com/small.jpg",
        src_portrait="https://example.com/portrait.jpg",
        src_landscape="https://example.com/landscape.jpg",
        src_tiny="https://example.com/tiny.jpg",
        alt="Test photo",
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


def test_list_photos_unauthenticated(client, test_photo):
    """Test listing photos without authentication."""
    response = client.get("/photos/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_photos_authenticated(client, test_photo, auth_headers):
    """Test listing photos with authentication."""
    response = client.get("/photos/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total" in data
    assert "photos" in data
    assert len(data["photos"]) == 1
    assert data["photos"][0]["id"] == test_photo.id


def test_list_photos_pagination(client, auth_headers, db):
    """Test photo listing pagination."""
    # Create multiple photos
    for i in range(25):
        photo = Photo(
            width=1920,
            height=1080,
            url=f"https://example.com/photo{i}",
            photographer="Test Photographer",
            photographer_url="https://example.com/photographer",
            photographer_id=123,
            avg_color="#FFFFFF",
            src_original=f"https://example.com/original{i}.jpg",
            src_large2x=f"https://example.com/large2x{i}.jpg",
            src_large=f"https://example.com/large{i}.jpg",
            src_medium=f"https://example.com/medium{i}.jpg",
            src_small=f"https://example.com/small{i}.jpg",
            src_portrait=f"https://example.com/portrait{i}.jpg",
            src_landscape=f"https://example.com/landscape{i}.jpg",
            src_tiny=f"https://example.com/tiny{i}.jpg",
            alt=f"Test photo {i}",
        )
        db.add(photo)
    db.commit()

    # Test first page
    response = client.get("/photos/?page=1&page_size=10", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 25
    assert data["page"] == 1
    assert len(data["photos"]) == 10

    # Test second page
    response = client.get("/photos/?page=2&page_size=10", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["page"] == 2
    assert len(data["photos"]) == 10


def test_get_photo_by_id(client, test_photo, auth_headers):
    """Test getting a specific photo by ID."""
    response = client.get(f"/photos/{test_photo.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_photo.id
    assert data["photographer"] == test_photo.photographer


def test_get_nonexistent_photo(client, auth_headers):
    """Test getting a non-existent photo."""
    response = client.get("/photos/99999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_photo_as_user(client, auth_headers):
    """Test that regular users cannot create photos."""
    photo_data = {
        "width": 1920,
        "height": 1080,
        "url": "https://example.com/photo",
        "photographer": "Test Photographer",
        "photographer_url": "https://example.com/photographer",
        "photographer_id": 123,
        "avg_color": "#FFFFFF",
        "src_original": "https://example.com/original.jpg",
        "src_large2x": "https://example.com/large2x.jpg",
        "src_large": "https://example.com/large.jpg",
        "src_medium": "https://example.com/medium.jpg",
        "src_small": "https://example.com/small.jpg",
        "src_portrait": "https://example.com/portrait.jpg",
        "src_landscape": "https://example.com/landscape.jpg",
        "src_tiny": "https://example.com/tiny.jpg",
        "alt": "Test photo",
    }
    response = client.post("/photos/", json=photo_data, headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_photo_as_admin(client, admin_headers):
    """Test creating a photo as admin."""
    photo_data = {
        "width": 1920,
        "height": 1080,
        "url": "https://example.com/photo",
        "photographer": "Test Photographer",
        "photographer_url": "https://example.com/photographer",
        "photographer_id": 123,
        "avg_color": "#FFFFFF",
        "src_original": "https://example.com/original.jpg",
        "src_large2x": "https://example.com/large2x.jpg",
        "src_large": "https://example.com/large.jpg",
        "src_medium": "https://example.com/medium.jpg",
        "src_small": "https://example.com/small.jpg",
        "src_portrait": "https://example.com/portrait.jpg",
        "src_landscape": "https://example.com/landscape.jpg",
        "src_tiny": "https://example.com/tiny.jpg",
        "alt": "Test photo",
    }
    response = client.post("/photos/", json=photo_data, headers=admin_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["photographer"] == "Test Photographer"


def test_update_photo_as_admin(client, test_photo, admin_headers):
    """Test updating a photo as admin."""
    update_data = {"alt": "Updated alt text"}
    response = client.patch(
        f"/photos/{test_photo.id}",
        json=update_data,
        headers=admin_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["alt"] == "Updated alt text"


def test_delete_photo_as_admin(client, test_photo, admin_headers):
    """Test deleting a photo as admin."""
    response = client.delete(f"/photos/{test_photo.id}", headers=admin_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_filter_photos_by_photographer(client, auth_headers, db):
    """Test filtering photos by photographer."""
    # Create photos with different photographers
    photo1 = Photo(
        width=1920,
        height=1080,
        url="https://example.com/photo1",
        photographer="John Doe",
        photographer_url="https://example.com/john",
        photographer_id=1,
        src_original="https://example.com/original1.jpg",
        src_large2x="https://example.com/large2x1.jpg",
        src_large="https://example.com/large1.jpg",
        src_medium="https://example.com/medium1.jpg",
        src_small="https://example.com/small1.jpg",
        src_portrait="https://example.com/portrait1.jpg",
        src_landscape="https://example.com/landscape1.jpg",
        src_tiny="https://example.com/tiny1.jpg",
    )
    photo2 = Photo(
        width=1920,
        height=1080,
        url="https://example.com/photo2",
        photographer="Jane Smith",
        photographer_url="https://example.com/jane",
        photographer_id=2,
        src_original="https://example.com/original2.jpg",
        src_large2x="https://example.com/large2x2.jpg",
        src_large="https://example.com/large2.jpg",
        src_medium="https://example.com/medium2.jpg",
        src_small="https://example.com/small2.jpg",
        src_portrait="https://example.com/portrait2.jpg",
        src_landscape="https://example.com/landscape2.jpg",
        src_tiny="https://example.com/tiny2.jpg",
    )
    db.add(photo1)
    db.add(photo2)
    db.commit()

    response = client.get("/photos/?photographer=John", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 1
    assert data["photos"][0]["photographer"] == "John Doe"
