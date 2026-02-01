from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional, List


class PhotoBase(BaseModel):
    """Base photo schema."""

    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    url: str
    photographer: str
    photographer_url: str
    photographer_id: int
    avg_color: Optional[str] = None
    alt: Optional[str] = None


class PhotoCreate(PhotoBase):
    """Schema for creating a new photo."""

    src_original: str
    src_large2x: str
    src_large: str
    src_medium: str
    src_small: str
    src_portrait: str
    src_landscape: str
    src_tiny: str


class PhotoUpdate(BaseModel):
    """Schema for updating a photo."""

    alt: Optional[str] = None
    photographer: Optional[str] = None


class PhotoResponse(PhotoCreate):
    """Schema for photo response."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PhotoList(BaseModel):
    """Schema for paginated photo list."""

    total: int
    page: int
    page_size: int
    photos: List[PhotoResponse]


class PhotoFilter(BaseModel):
    """Schema for photo filtering."""

    photographer: Optional[str] = None
    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None
    search: Optional[str] = None
