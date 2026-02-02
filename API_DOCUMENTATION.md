# Photo Management API Documentation

## Base URL
```
http://localhost:8000
```
## Swagger Documentation
```
http://localhost:8000/api/docs
```

## Authentication

All endpoints except `/auth/register`, `/auth/login`, and `/health` require authentication using JWT Bearer tokens.

Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```
**Options for getting a bearer token:**
1. Login with the default admin credentials and use provided bearer token
2. Register a new user, login, and then use the provided bearer token.

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "username": "username",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Refresh Token
```http
POST /auth/refresh?refresh_token=<refresh_token>
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Photos

#### List Photos
```http
GET /photos/?page=1&page_size=20&photographer=John&min_width=1920&search=beach
```

**Query Parameters:**
- `page` (integer, default: 1): Page number
- `page_size` (integer, default: 20, max: 100): Items per page
- `photographer` (string, optional): Filter by photographer name
- `min_width` (integer, optional): Minimum width
- `max_width` (integer, optional): Maximum width
- `min_height` (integer, optional): Minimum height
- `max_height` (integer, optional): Maximum height
- `search` (string, optional): Search in alt text and photographer

**Response:** `200 OK`
```json
{
  "total": 100,
  "page": 1,
  "page_size": 20,
  "photos": [
    {
      "id": 1,
      "width": 1920,
      "height": 1080,
      "url": "https://www.pexels.com/photo/...",
      "photographer": "John Doe",
      "photographer_url": "https://www.pexels.com/@john-doe",
      "photographer_id": 123,
      "avg_color": "#FFFFFF",
      "src_original": "https://images.pexels.com/.../original.jpg",
      "src_large2x": "https://images.pexels.com/.../large2x.jpg",
      "src_large": "https://images.pexels.com/.../large.jpg",
      "src_medium": "https://images.pexels.com/.../medium.jpg",
      "src_small": "https://images.pexels.com/.../small.jpg",
      "src_portrait": "https://images.pexels.com/.../portrait.jpg",
      "src_landscape": "https://images.pexels.com/.../landscape.jpg",
      "src_tiny": "https://images.pexels.com/.../tiny.jpg",
      "alt": "Beautiful sunset at the beach",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

#### Get Photo by ID
```http
GET /photos/{photo_id}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "width": 1920,
  "height": 1080,
  "url": "https://www.pexels.com/photo/...",
  "photographer": "John Doe",
  ...
}
```

#### Create Photo (Admin Only)
```http
POST /photos/
```

**Request Body:**
```json
{
  "width": 1920,
  "height": 1080,
  "url": "https://www.pexels.com/photo/...",
  "photographer": "John Doe",
  "photographer_url": "https://www.pexels.com/@john-doe",
  "photographer_id": 123,
  "avg_color": "#FFFFFF",
  "src_original": "https://images.pexels.com/.../original.jpg",
  "src_large2x": "https://images.pexels.com/.../large2x.jpg",
  "src_large": "https://images.pexels.com/.../large.jpg",
  "src_medium": "https://images.pexels.com/.../medium.jpg",
  "src_small": "https://images.pexels.com/.../small.jpg",
  "src_portrait": "https://images.pexels.com/.../portrait.jpg",
  "src_landscape": "https://images.pexels.com/.../landscape.jpg",
  "src_tiny": "https://images.pexels.com/.../tiny.jpg",
  "alt": "Beautiful sunset at the beach"
}
```

**Response:** `201 Created`

#### Update Photo (Admin Only)
```http
PATCH /photos/{photo_id}
```

**Request Body (all fields optional for partial updates):**
```json
{
  "width": 2560,
  "height": 1440,
  "url": "https://www.pexels.com/photo/...",
  "photographer": "Updated Name",
  "photographer_url": "https://www.pexels.com/@updated-name",
  "photographer_id": 456,
  "avg_color": "#000000",
  "src_original": "https://images.pexels.com/.../original.jpg",
  "src_large2x": "https://images.pexels.com/.../large2x.jpg",
  "src_large": "https://images.pexels.com/.../large.jpg",
  "src_medium": "https://images.pexels.com/.../medium.jpg",
  "src_small": "https://images.pexels.com/.../small.jpg",
  "src_portrait": "https://images.pexels.com/.../portrait.jpg",
  "src_landscape": "https://images.pexels.com/.../landscape.jpg",
  "src_tiny": "https://images.pexels.com/.../tiny.jpg",
  "alt": "Updated description"
}
```

**Note:** All fields are optional. You can update any combination of fields in a single request.

**Response:** `200 OK` (Returns the updated photo object)

#### Delete Photo (Admin Only)
```http
DELETE /photos/{photo_id}
```

**Response:** `204 No Content`

#### Get Photos by Photographer
```http
GET /photos/photographer/{photographer_id}?page=1&page_size=20
```

**Response:** `200 OK` (Same format as List Photos)

### Health

#### Basic Health Check
```http
GET /health/
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "Photo Management API"
}
```

#### Database Health Check
```http
GET /health/db
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "An internal server error occurred",
  "type": "internal_server_error"
}
```

## Rate Limiting

The API implements rate limiting of 60 requests per minute per user (configurable).

## Interactive Documentation

FastAPI provides interactive API documentation:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
