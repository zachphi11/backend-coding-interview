from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from sqlalchemy import text

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():
    """
    Basic health check endpoint.

    Returns the API status.
    """
    return {"status": "healthy", "service": "Photo Management API"}


@router.get("/db")
def database_health_check(db: Session = Depends(get_db)):
    """
    Database health check endpoint.

    Verifies database connectivity.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
