from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.photo import Photo
from app.schemas.photo import PhotoCreate, PhotoUpdate, PhotoFilter


class PhotoService:
    """Service for photo-related operations."""

    @staticmethod
    def create_photo(db: Session, photo_data: PhotoCreate) -> Photo:
        """Create a new photo."""
        photo = Photo(**photo_data.model_dump())
        db.add(photo)
        db.commit()
        db.refresh(photo)
        return photo

    @staticmethod
    def get_photo_by_id(db: Session, photo_id: int) -> Photo:
        """Get photo by ID."""
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if not photo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photo not found",
            )
        return photo

    @staticmethod
    def get_photos(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        filters: Optional[PhotoFilter] = None,
    ) -> tuple[List[Photo], int]:
        """Get list of photos with optional filtering."""
        query = db.query(Photo)

        # Apply filters if provided
        if filters:
            if filters.photographer:
                query = query.filter(
                    Photo.photographer.ilike(f"%{filters.photographer}%")
                )

            if filters.min_width:
                query = query.filter(Photo.width >= filters.min_width)

            if filters.max_width:
                query = query.filter(Photo.width <= filters.max_width)

            if filters.min_height:
                query = query.filter(Photo.height >= filters.min_height)

            if filters.max_height:
                query = query.filter(Photo.height <= filters.max_height)

            if filters.search:
                search_term = f"%{filters.search}%"
                query = query.filter(
                    or_(
                        Photo.alt.ilike(search_term),
                        Photo.photographer.ilike(search_term),
                    )
                )

        # Get total count
        total = query.count()

        # Get paginated results
        photos = query.order_by(Photo.created_at.desc()).offset(skip).limit(limit).all()

        return photos, total

    @staticmethod
    def update_photo(db: Session, photo_id: int, photo_data: PhotoUpdate) -> Photo:
        """Update a photo."""
        photo = PhotoService.get_photo_by_id(db, photo_id)

        update_data = photo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(photo, field, value)

        db.commit()
        db.refresh(photo)
        return photo

    @staticmethod
    def delete_photo(db: Session, photo_id: int) -> None:
        """Delete a photo."""
        photo = PhotoService.get_photo_by_id(db, photo_id)
        db.delete(photo)
        db.commit()

    @staticmethod
    def get_photos_by_photographer(
        db: Session, photographer_id: int, skip: int = 0, limit: int = 20
    ) -> tuple[List[Photo], int]:
        """Get photos by photographer ID."""
        query = db.query(Photo).filter(Photo.photographer_id == photographer_id)
        total = query.count()
        photos = query.order_by(Photo.created_at.desc()).offset(skip).limit(limit).all()
        return photos, total
