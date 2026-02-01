"""
Script to ingest photo data from photos.csv into the database.
"""
import csv
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.photo import Photo
from app.models.user import User
from app.core.security import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_admin_user(db: Session):
    """Create a default admin user if it doesn't exist."""
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        logger.info("Created admin user (username: admin, password: admin123)")
    else:
        logger.info("Admin user already exists")


def ingest_photos(csv_path: str, db: Session):
    """Ingest photos from CSV file into the database."""
    try:
        with open(csv_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            count = 0

            for row in csv_reader:
                # Check if photo already exists
                existing_photo = db.query(Photo).filter(Photo.id == int(row["id"])).first()
                if existing_photo:
                    logger.debug(f"Photo {row['id']} already exists, skipping")
                    continue

                # Create photo object
                photo = Photo(
                    id=int(row["id"]),
                    width=int(row["width"]),
                    height=int(row["height"]),
                    url=row["url"],
                    photographer=row["photographer"],
                    photographer_url=row["photographer_url"],
                    photographer_id=int(row["photographer_id"]),
                    avg_color=row["avg_color"],
                    src_original=row["src.original"],
                    src_large2x=row["src.large2x"],
                    src_large=row["src.large"],
                    src_medium=row["src.medium"],
                    src_small=row["src.small"],
                    src_portrait=row["src.portrait"],
                    src_landscape=row["src.landscape"],
                    src_tiny=row["src.tiny"],
                    alt=row["alt"],
                )

                db.add(photo)
                count += 1

                # Commit in batches of 100
                if count % 100 == 0:
                    db.commit()
                    logger.info(f"Ingested {count} photos")

            # Commit remaining photos
            db.commit()
            logger.info(f"Successfully ingested {count} photos from {csv_path}")

    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_path}")
        raise
    except Exception as e:
        logger.error(f"Error ingesting photos: {e}")
        db.rollback()
        raise


def main():
    """Main function to run the ingestion script."""
    # Create tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    # Create database session
    db = SessionLocal()

    try:
        # Create admin user
        logger.info("Creating admin user...")
        create_admin_user(db)

        # Ingest photos
        csv_path = Path(__file__).parent.parent / "photos.csv"
        logger.info(f"Starting photo ingestion from {csv_path}")
        ingest_photos(str(csv_path), db)

        logger.info("Ingestion completed successfully!")

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
