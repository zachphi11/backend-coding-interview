# Setup Instructions

## Prerequisites
- Docker

## Docker Launch
### 1. Create environment file
```bash
cp .env.example .env
```

### 2. Start the application
```bash
docker-compose up --build
```

The application will:
- Start PostgreSQL database
- Run database migrations
- Ingest photo data from photos.csv
- Start the API server on http://localhost:8000

### 3. Access the API
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

### 4. Default Admin Credentials
```
Username: admin
Password: admin123
```
**Credentials to be changed and stored in Secrets Manager in production**

## Running Tests

### With Docker

#### If API is already running
In a separate terminal:
```bash
docker-compose exec api pytest
```
#### IF API is NOT running (running tests independently)
```bash
docker-compose run --rm api pytest --cov=app --cov-report=html
```

### Locally
```bash
pytest
```

### With coverage
```bash
pytest --cov=app --cov-report=html
```

View coverage report: `htmlcov/index.html`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Photo Management API |
| `DEBUG` | Debug mode | False |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration | 7 |
| `CORS_ORIGINS` | Allowed CORS origins | ["http://localhost:3000"] |
| `DEFAULT_PAGE_SIZE` | Default pagination size | 20 |
| `MAX_PAGE_SIZE` | Maximum pagination size | 100 |

