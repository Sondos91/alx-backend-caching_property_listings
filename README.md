# ALX Backend Caching Property Listings

A Django-based property listing application with Redis caching and PostgreSQL database, designed to demonstrate efficient data caching strategies.

## Features

- **Django 4.2.7** web framework
- **PostgreSQL** database for persistent storage
- **Redis** for high-performance caching
- **Property Management** with full CRUD operations
- **Admin Interface** for easy property management
- **Caching Layer** for improved performance

## Project Structure

```
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/  # Django project settings
├── properties/                             # Property management app
│   ├── models.py                          # Property model definition
│   ├── views.py                           # API views with caching
│   ├── admin.py                           # Admin interface configuration
│   ├── urls.py                            # URL routing
│   └── management/                        # Custom management commands
├── docker-compose.yml                     # Docker services configuration
├── requirements.txt                       # Python dependencies
├── manage.py                              # Django management script
└── README.md                              # This file
```

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- pip (Python package manager)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd alx-backend-caching_property_listings
```

### 2. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Start Docker Services

```bash
docker-compose up -d
```

This will start:
- **PostgreSQL** on port 5432
- **Redis** on port 6379

### 4. Run Database Migrations

```bash
python3 manage.py migrate
```

### 5. Create Sample Data (Optional)

```bash
python3 manage.py create_sample_properties
```

### 6. Create Superuser (Optional)

```bash
python3 manage.py createsuperuser
```

### 7. Start Development Server

```bash
python3 manage.py runserver
```

The application will be available at `http://localhost:8000`

## Configuration

### Database Configuration

The application is configured to use PostgreSQL with the following settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'property_db',
        'USER': 'property_user',
        'PASSWORD': 'property_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Redis Cache Configuration

Redis is configured as the cache backend:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## API Endpoints

### Property Management

- **GET** `/properties/list/` - List all properties (with caching)
- **GET** `/properties/test-cache/` - Test Redis caching functionality

### Admin Interface

- **GET** `/admin/` - Django admin interface for property management

## Property Model

The Property model includes the following fields:

- `title` (CharField, max_length=200) - Property title
- `description` (TextField) - Detailed property description
- `price` (DecimalField, max_digits=10, decimal_places=2) - Property price
- `location` (CharField, max_length=100) - Property location
- `created_at` (DateTimeField, auto_now_add=True) - Creation timestamp

## Caching Strategy

The application implements a two-tier caching strategy:

1. **Property List Caching**: Property listings are cached for 5 minutes to reduce database queries
2. **Test Cache**: Simple cache test endpoint with 60-second expiration
3. **Session Storage**: User sessions are stored in Redis for improved performance

## Docker Services

### PostgreSQL Service

- **Image**: `postgres:latest`
- **Port**: 5432
- **Database**: `property_db`
- **Username**: `property_user`
- **Password**: `property_password`

### Redis Service

- **Image**: `redis:latest`
- **Port**: 6379
- **Database**: 1 (for Django cache)

## Development

### Running Tests

```bash
python3 manage.py test
```

### Checking System Status

```bash
python3 manage.py check
```

### Database Shell

```bash
python3 manage.py dbshell
```

### Django Shell

```bash
python3 manage.py shell
```

## Performance Benefits

- **Reduced Database Load**: Frequently accessed data is served from Redis cache
- **Faster Response Times**: Cached responses eliminate database query overhead
- **Scalability**: Redis can handle high concurrent read operations
- **Session Management**: User sessions are stored in Redis for better performance

## Troubleshooting

### Common Issues

1. **Docker Connection Error**: Ensure Docker is running and accessible
2. **Database Connection**: Verify PostgreSQL service is running on port 5432
3. **Cache Issues**: Check Redis service status and clear cache if needed
4. **Migration Errors**: Ensure all dependencies are installed and database is accessible

### Useful Commands

```bash
# Check Docker services status
docker-compose ps

# View Docker logs
docker-compose logs postgres
docker-compose logs redis

# Clear Django cache
python3 manage.py shell -c "from django.core.cache import cache; cache.clear()"

# Restart Docker services
docker-compose restart
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the ALX Backend Development curriculum.

## Support

For questions or issues, please refer to the project documentation or contact the development team.
