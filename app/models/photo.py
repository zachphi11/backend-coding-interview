from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime
from app.db.database import Base


class Photo(Base):
    """Photo model representing images from Pexels."""

    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    photographer = Column(String, nullable=False, index=True)
    photographer_url = Column(String, nullable=False)
    photographer_id = Column(Integer, nullable=False, index=True)
    avg_color = Column(String, nullable=True)

    # Image sources
    src_original = Column(String, nullable=False)
    src_large2x = Column(String, nullable=False)
    src_large = Column(String, nullable=False)
    src_medium = Column(String, nullable=False)
    src_small = Column(String, nullable=False)
    src_portrait = Column(String, nullable=False)
    src_landscape = Column(String, nullable=False)
    src_tiny = Column(String, nullable=False)

    # Metadata
    alt = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Composite indexes for common queries
    __table_args__ = (
        Index("idx_photographer_created", "photographer", "created_at"),
        Index("idx_dimensions", "width", "height"),
    )

    def __repr__(self):
        return f"<Photo {self.id} by {self.photographer}>"
