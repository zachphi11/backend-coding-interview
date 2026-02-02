# Photo Management API - Project Documentation

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture Decisions](#architecture-decisions)
- [Features Implemented](#features-implemented)
- [What I Would Add With More Time](#what-i-would-add-with-more-time)
- [Assumptions Made](#assumptions-made)

## Quick Start

### Using Docker (Recommended)
```bash
docker-compose up --build
```

Visit http://localhost:8000/api/docs for interactive API documentation.

**Default Admin Credentials (Should be stored in Secrets Manager in Production):**
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
- **Denormalized photographer data**: Small dataset so it felt unnecessary to normalize the data. Kept photographer info in photos table for faster reads.
- **Composite indexes**: Created indexes on common query patterns (photographer + created_at, photo dimensions)
- **Separate users table**: Proper authentication requires isolated user management

### 3. Authentication: JWT (JSON Web Tokens)

**Why JWT?**
- **Stateless**: No server-side session storage required
- **Scalable**: Easy to scale horizontally
- **Standard**: Industry-standard approach

**Implementation Details:**
- Access tokens: 30-minute expiration for security
- Refresh tokens: 7-day expiration for user experience
- Bearer token authentication
- Password hashing with bcrypt

**Trade-offs:**
- Cannot revoke tokens before expiration (mitigated with short expiration)
- Requires secure secret key management

### 4. Project Structure: Layered Architecture

```
app/
|-- api/          # API endpoints 
|-- core/         # Core functionality (config, security, dependencies)
|-- db/           # Database configuration
|-- models/       # SQLAlchemy models
|-- schemas/      # Pydantic schemas (API model validation)
|-- services/     # Business logic layer
```

**Benefits:**
- **Separation of Concerns**: Each layer has a clear responsibility
- **Testability**: Easy to mock and test individual layers
- **Maintainability**: Changes are localized to specific layers
- **Scalability**: Easy to add new features without affecting existing code


## Features Implemented

**Feature Implementation reasoning:**  
When choosing what features to implement, I firstly focused on the core functionality and must-haves of the application: data ingestion, database design, authentication, basic api endpoints for photos, testing, and usability. After that I focused on nice to haves like filtering on the photos and admin versus user actions.

### Features:

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
   - Auto-generated Swagger docs
   - Detailed API documentation in [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

5. **Testing**
   - Unit tests for all endpoints
   - Authentication tests
   - Authorization tests
   - Filter and pagination tests
   - Test coverage reporting


## What I Would Add With More Time

1. **TDD or BDD approach**
   - Chose to implement first and then write tests for speed
   - Implement Red - Green - Refactor for TDD
   - Alternatively use pytest-bdd framework

2. **Database Migrations**
   - Alembic for schema versioning
   - Migration scripts
   - Rollback capability

3. **Logging**
   - Structured logging
   - Request/response logging
   - Error tracking

4. **API Versioning**
    - `/api/v1/` prefix
    - Backward compatibility
    - Deprecation strategy

## Assumptions Made

1. **Read-Heavy Workload** -  More reads than writes

2. **Public Photo Data** - All authenticated users can view all photos

3. **Admin Priveleges** - Only admins will be able to add, update, or delete from the database

4. **CSV Data is Clean** - photos.csv has valid data

5. **Photo IDs are Unique** - Pexels IDs are unique

## Technology Stack

- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)us
- **Password Hashing**: bcrypt
- **Testing**: pytest
- **Containerization**: Docker & Docker Compose
- **Web Server**: Uvicorn

