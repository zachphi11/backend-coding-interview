from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.schemas.photo import PhotoCreate, PhotoResponse, PhotoUpdate, PhotoList, PhotoFilter
from app.services.photo_service import PhotoService
from app.core.dependencies import get_current_user, get_current_admin_user
from app.models.user import User
from app.core.config import settings

router = APIRouter(prefix="/photos", tags=["Photos"])


@router.post(
    "/",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
def create_photo(photo_data: PhotoCreate, db: Session = Depends(get_db)):
    """
    Create a new photo (Admin only).

    Requires admin authentication.
    """
    return PhotoService.create_photo(db, photo_data)


@router.get("/", response_model=PhotoList)
def list_photos(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Number of items per page",
    ),
    photographer: Optional[str] = Query(None, description="Filter by photographer name"),
    min_width: Optional[int] = Query(None, ge=0, description="Minimum width"),
    max_width: Optional[int] = Query(None, ge=0, description="Maximum width"),
    min_height: Optional[int] = Query(None, ge=0, description="Minimum height"),
    max_height: Optional[int] = Query(None, ge=0, description="Maximum height"),
    search: Optional[str] = Query(None, description="Search in alt text and photographer"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all photos with pagination and optional filtering.

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    - **photographer**: Filter by photographer name
    - **min_width**: Filter by minimum width
    - **max_width**: Filter by maximum width
    - **min_height**: Filter by minimum height
    - **max_height**: Filter by maximum height
    - **search**: Search in alt text and photographer name

    Requires authentication.
    """
    skip = (page - 1) * page_size

    filters = PhotoFilter(
        photographer=photographer,
        min_width=min_width,
        max_width=max_width,
        min_height=min_height,
        max_height=max_height,
        search=search,
    )

    photos, total = PhotoService.get_photos(db, skip=skip, limit=page_size, filters=filters)

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "photos": photos,
    }


@router.get("/{photo_id}", response_model=PhotoResponse)
def get_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific photo by ID.

    - **photo_id**: Photo ID

    Requires authentication.
    """
    return PhotoService.get_photo_by_id(db, photo_id)


@router.patch(
    "/{photo_id}",
    response_model=PhotoResponse,
    dependencies=[Depends(get_current_admin_user)],
)
def update_photo(
    photo_id: int,
    photo_data: PhotoUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a photo (Admin only).

    - **photo_id**: Photo ID
    - **alt**: New alt text (optional)
    - **photographer**: New photographer name (optional)

    Requires admin authentication.
    """
    return PhotoService.update_photo(db, photo_id, photo_data)


@router.delete(
    "/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    """
    Delete a photo (Admin only).

    - **photo_id**: Photo ID

    Requires admin authentication.
    """
    PhotoService.delete_photo(db, photo_id)


@router.get("/photographer/{photographer_id}", response_model=PhotoList)
def get_photos_by_photographer(
    photographer_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all photos by a specific photographer.

    - **photographer_id**: Photographer ID
    - **page**: Page number
    - **page_size**: Number of items per page

    Requires authentication.
    """
    skip = (page - 1) * page_size
    photos, total = PhotoService.get_photos_by_photographer(
        db, photographer_id, skip=skip, limit=page_size
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "photos": photos,
    }
