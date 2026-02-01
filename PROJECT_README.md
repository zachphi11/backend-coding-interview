# Photo Management API - Project Documentation

## Overview

A production-ready RESTful API for managing photo data from Pexels, built with FastAPI and PostgreSQL. This project demonstrates best practices in API design, authentication, testing, and deployment.

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture Decisions](#architecture-decisions)
- [Features Implemented](#features-implemented)
- [API Design](#api-design)
- [Database Schema](#database-schema)
- [Security Considerations](#security-considerations)
- [Testing Strategy](#testing-strategy)
- [What I Would Add With More Time](#what-i-would-add-with-more-time)
- [Assumptions Made](#assumptions-made)

## Quick Start

### Using Docker (Recommended)
```bash
docker-compose up --build
```

Visit http://localhost:8000/api/docs for interactive API documentation.

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

For detailed setup instructions, see [SETUP.md](SETUP.md).

## Architecture Decisions

### 1. Framework Choice: FastAPI

**Why FastAPI?**
- **Familiarity**: It's the framework I'm most comfortable with at the moment
- **Performance**: One of the fastest Python frameworks
- **Auto Documentation**: Automatic OpenAPI/Swagger documentation generation
- **Type Safety**: Built-in Pydantic validation reduces bugs
- **Async Support**: Native async/await support for high concurrency

**Trade-offs:**
- Smaller ecosystem compared to Django
- Less built-in features, but that makes it lightweight
- Requires more manual configuration for complex use cases

### 2. Database: PostgreSQL

**Why PostgreSQL?**
- **Production Ready**: Industry standard for production applications
- **ACID Compliance**: Guarantees data integrity
- **Advanced Features**: Full-text search, JSON support, robust indexing
- **Scalability**: Handles millions of records efficiently
- **Free & Open Source**: No licensing costs

**Schema Design Decisions:**
- **Denormalized photographer data**: Kept photographer info in photos table for faster reads (read-heavy workload assumption)
- **Composite indexes**: Created indexes on common query patterns (photographer + created_at, dimensions)
- **Separate users table**: Proper authentication requires isolated user management

### 3. Authentication: JWT (JSON Web Tokens)

**Why JWT?**
- **Stateless**: No server-side session storage required
- **Scalable**: Easy to scale horizontally
- **Standard**: Industry-standard approach
- **Mobile-Friendly**: Works well with mobile apps and SPAs

**Implementation Details:**
- Access tokens: 30-minute expiration (security)
- Refresh tokens: 7-day expiration (user experience)
- Bearer token authentication
- Password hashing with bcrypt

**Trade-offs:**
- Cannot revoke tokens before expiration (mitigated with short expiration)
- Token size larger than session IDs
- Requires secure secret key management

### 4. Project Structure: Layered Architecture

```
app/
├── api/          # API endpoints (routes)
├── core/         # Core functionality (config, security, dependencies)
├── db/           # Database configuration
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas (validation)
└── services/     # Business logic layer
```

**Benefits:**
- **Separation of Concerns**: Each layer has a clear responsibility
- **Testability**: Easy to mock and test individual layers
- **Maintainability**: Changes are localized to specific layers
- **Scalability**: Easy to add new features without affecting existing code

### 5. Dependency Management

**Why requirements.txt?**
- Simple and standard for Python projects
- Easy to understand and maintain
- Works with all deployment platforms

**Alternative considered:** Poetry (more complex, overkill for this project)

## Features Implemented

### Core Requirements

1. **Data Ingestion**
   - CSV parsing with error handling
   - Batch processing (100 records at a time)
   - Duplicate detection
   - Automatic admin user creation

2. **Authentication & Authorization**
   - User registration with validation
   - Login with JWT tokens
   - Token refresh mechanism
   - Role-based access control (Admin vs User)
   - Protected endpoints

3. **Photo Management API**
   - List photos with pagination
   - Get photo by ID
   - Filter by photographer, dimensions, search term
   - Create/Update/Delete (admin only)
   - Get photos by photographer

4. **API Documentation**
   - Auto-generated OpenAPI/Swagger docs
   - ReDoc alternative documentation
   - Detailed API documentation in [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

5. **Testing**
   - Unit tests for all endpoints
   - Authentication tests
   - Authorization tests
   - Filter and pagination tests
   - Test coverage reporting

### Production-Ready Features

1. **Error Handling**
   - Consistent error response format
   - HTTP status codes following REST standards
   - Detailed error messages for debugging
   - Global exception handler

2. **Database Design**
   - Proper indexing for performance
   - Composite indexes for common queries
   - Database connection pooling
   - Health check endpoint for database

3. **Security**
   - Password hashing (bcrypt)
   - JWT token authentication
   - CORS middleware
   - Input validation with Pydantic
   - SQL injection prevention (SQLAlchemy ORM)

4. **Code Quality**
   - Type hints throughout
   - Docstrings for all public functions
   - Consistent code style
   - Separation of concerns

5. **Deployment**
   - Docker configuration
   - Docker Compose for local development
   - Environment variable configuration
   - Health check endpoints
   - Makefile for common tasks

6. **Documentation**
   - Comprehensive README
   - Setup instructions
   - API documentation
   - Code comments where needed

## API Design

### RESTful Principles

1. **Resource-Based URLs**
   - `/photos/` - Photo collection
   - `/photos/{id}` - Individual photo
   - `/photos/photographer/{id}` - Nested resource

2. **HTTP Methods**
   - `GET` - Retrieve resources
   - `POST` - Create resources
   - `PATCH` - Partial update
   - `DELETE` - Remove resources

3. **Status Codes**
   - `200 OK` - Successful GET/PATCH
   - `201 Created` - Successful POST
   - `204 No Content` - Successful DELETE
   - `400 Bad Request` - Validation error
   - `401 Unauthorized` - Authentication required
   - `403 Forbidden` - Insufficient permissions
   - `404 Not Found` - Resource not found
   - `422 Unprocessable Entity` - Validation error

4. **Pagination**
   - Query parameters: `page`, `page_size`
   - Response includes metadata: `total`, `page`, `page_size`
   - Configurable defaults and limits

5. **Filtering**
   - Query parameters for common filters
   - Full-text search capability
   - Range filters (min/max dimensions)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

### Photos Table
```sql
CREATE TABLE photos (
    id INTEGER PRIMARY KEY,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    url VARCHAR NOT NULL,
    photographer VARCHAR NOT NULL,
    photographer_url VARCHAR NOT NULL,
    photographer_id INTEGER NOT NULL,
    avg_color VARCHAR,
    src_original VARCHAR NOT NULL,
    src_large2x VARCHAR NOT NULL,
    src_large VARCHAR NOT NULL,
    src_medium VARCHAR NOT NULL,
    src_small VARCHAR NOT NULL,
    src_portrait VARCHAR NOT NULL,
    src_landscape VARCHAR NOT NULL,
    src_tiny VARCHAR NOT NULL,
    alt VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_photos_photographer ON photos(photographer);
CREATE INDEX idx_photos_photographer_id ON photos(photographer_id);
CREATE INDEX idx_photos_alt ON photos(alt);
CREATE INDEX idx_photos_created_at ON photos(created_at);
CREATE INDEX idx_photographer_created ON photos(photographer, created_at);
CREATE INDEX idx_dimensions ON photos(width, height);
```

### Indexing Strategy

**Single Column Indexes:**
- `photographer`: Frequent filter/search
- `photographer_id`: Foreign key lookups
- `alt`: Text search
- `created_at`: Sorting

**Composite Indexes:**
- `(photographer, created_at)`: Common query pattern
- `(width, height)`: Dimension-based filtering

**Why These Indexes?**
- Photos are read-heavy (listing, filtering, searching)
- Trade-off: Slower writes, faster reads
- Assumption: More reads than writes in photo browsing application

## Security Considerations

### 1. Authentication
- JWT tokens with expiration
- Refresh token rotation
- Secure password hashing (bcrypt with salt)

### 2. Authorization
- Role-based access control
- Admin-only endpoints for sensitive operations
- User can only access their own data (if needed)

### 3. Input Validation
- Pydantic schemas validate all input
- Email validation
- Password strength requirements (min 8 characters)
- SQL injection prevention via ORM

### 4. CORS
- Configurable allowed origins
- Prevents unauthorized cross-origin requests

### 5. Environment Variables
- Sensitive data (SECRET_KEY, DATABASE_URL) in .env
- .env not committed to version control
- .env.example for reference

### 6. Dependencies
- Using well-maintained libraries
- Regular security updates needed

## Testing Strategy

### Test Coverage

1. **Unit Tests**
   - Individual functions and methods
   - Service layer logic
   - Model methods

2. **Integration Tests**
   - API endpoints
   - Database interactions
   - Authentication flow

3. **Test Fixtures**
   - Isolated test database (SQLite)
   - Reusable test data
   - Fresh database for each test

### Test Organization

```
tests/
├── conftest.py         # Fixtures and configuration
├── test_auth.py        # Authentication tests
├── test_photos.py      # Photo endpoint tests
└── test_health.py      # Health check tests
```

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_auth.py

# Verbose output
pytest -v
```

### What's Tested

- User registration (success, duplicates, validation)
- User login (success, invalid credentials)
- Token refresh
- Photo listing (pagination, filtering)
- Photo retrieval
- Photo creation (admin only)
- Photo updates (admin only)
- Photo deletion (admin only)
- Authorization checks
- Health checks

## What I Would Add With More Time

### High Priority

1. **Rate Limiting**
   - Implement with Redis
   - Per-user and per-IP limits
   - Configurable thresholds

2. **Caching**
   - Redis cache for frequently accessed photos
   - Cache invalidation strategy
   - Cache popular searches

3. **Full-Text Search**
   - PostgreSQL full-text search
   - Or integrate Elasticsearch
   - Search across all text fields

4. **Database Migrations**
   - Alembic for schema versioning
   - Migration scripts
   - Rollback capability

5. **Logging**
   - Structured logging (JSON)
   - Log aggregation (ELK stack)
   - Request/response logging
   - Error tracking (Sentry)

6. **Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - APM (Application Performance Monitoring)

### Medium Priority

7. **User Favorites**
   - Users can favorite photos
   - List user's favorites
   - Many-to-many relationship

8. **Photo Collections/Albums**
   - Users create collections
   - Add photos to collections
   - Share collections

9. **Advanced Filtering**
   - Color-based search
   - Aspect ratio filtering
   - Date range filtering

10. **API Versioning**
    - `/api/v1/` prefix
    - Backward compatibility
    - Deprecation strategy

11. **Background Jobs**
    - Celery for async tasks
    - Image processing
    - Batch operations

12. **File Upload**
    - S3 integration
    - Image upload endpoint
    - Thumbnail generation

### Lower Priority

13. **Email Notifications**
    - Email verification
    - Password reset
    - SendGrid integration

14. **OAuth Integration**
    - Google login
    - GitHub login
    - Social authentication

15. **GraphQL API**
    - Alternative to REST
    - Flexible queries
    - Strawberry or Graphene

16. **Webhooks**
    - Notify on new photos
    - Notify on updates
    - Configurable webhooks

17. **Admin Dashboard**
    - Web UI for admin tasks
    - User management
    - Photo moderation

18. **Analytics**
    - Track popular photos
    - User engagement metrics
    - Search analytics

## Assumptions Made

### Business Logic

1. **Read-Heavy Workload**
   - Assumption: More reads than writes
   - Impact: Optimized for read performance, denormalized data

2. **Public Photo Data**
   - Assumption: All authenticated users can view all photos
   - Impact: No photo-level permissions (only admin for modifications)

3. **Single Admin Role**
   - Assumption: Two-tier access (admin vs user)
   - Impact: Simple RBAC, could expand to more roles

### Technical

4. **PostgreSQL Available**
   - Assumption: PostgreSQL is acceptable for deployment
   - Alternative: Could use MySQL or SQLite (dev only)

5. **Synchronous Operations Acceptable**
   - Assumption: Response times under 200ms acceptable
   - Alternative: Could add async processing for heavy operations

6. **Single Server Deployment Initially**
   - Assumption: Starting with single-instance deployment
   - Future: Could scale horizontally with load balancer

### Data

7. **CSV Data is Clean**
   - Assumption: photos.csv has valid data
   - Impact: Basic validation, could add more robust error handling

8. **Photo IDs are Unique**
   - Assumption: Pexels IDs won't collide
   - Impact: Using CSV ID as primary key

9. **Photographer Data Denormalized**
   - Assumption: Photographer info changes rarely
   - Impact: Faster queries, potential data inconsistency if photographer info updates

## Technology Stack

- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Testing**: pytest
- **Containerization**: Docker & Docker Compose
- **Web Server**: Uvicorn

