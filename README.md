# Docker-Based Solar Project

This repository contains a Docker-based setup for a solar project with a backend, PostgreSQL database, and Nginx configuration for production deployment.

## Project Structure

```
.
├── README.md                 # Documentation
├── config                    # PostgreSQL configuration files
│   ├── pg_hba.conf           # PostgreSQL host-based authentication config
│   └── postgresql.conf       # PostgreSQL main config file
├── docker-compose.dev.yml    # Docker Compose file for development
├── docker-compose.prod.yml   # Docker Compose file for production
├── nginx                     # Nginx configuration directory
│   └── default.conf          # Nginx configuration file
└── project_backend           # Django backend project
    ├── Dockerfile            # Docker configuration for backend
    ├── core                  # Core application directory
    ├── env                   # Environment variables
    ├── manage.py             # Django management script
    ├── project_backend       # Django project directory
    ├── requirements.txt      # Python dependencies
    └── user                  # User module
```

---

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

### 1. Clone the repository

```sh
git clone <repository-url>
cd docker_base_solar_project
```

### 2. Environment Variables

Create an `.env.dev` for ddevelopment and `.env.prod` for production file in the `project_backend` directory and set the required environment variables:

```
# Database Configuration (example)
POSTGRES_USER=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=5432
POSTGRES_PASSWORD=

# Django Configuration
DJANGO_DEBUG=
DJANGO_ALLOWED_HOSTS=

# Security & CORS
CORS_ALLOWED_ORIGINS=
CSRF_TRUSTED_ORIGINS=
# Important: The SECRET_KEY is stored securely in Docker Secrets
DJANGO_SECRET_KEY=Stored_securely_in_Docker_Secrets
```

```
# Database Configuration (development example)
POSTGRES_USER=dev_database_user
POSTGRES_DB=dev_database_name
POSTGRES_HOST=postgres-db-dev
POSTGRES_PORT=5432
POSTGRES_PASSWORD=solar_password
# Important: The password is stored as a Docker Secret, not here!
# POSTGRES_PASSWORD= (Stored securely in Docker Secrets)

# Django Configuration
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1

# Security & CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000

# Important: The SECRET_KEY is stored as a Docker Secret, not here!
DJANGO_SECRET_KEY= 'django-insecure-#q2z3g*ro$@u9z(nry5!z^$4=z6l9v(6r(d3t=bab3@70$r$t!'
```

### 3. Running in Development Mode

To start the project in development mode:

```sh
docker-compose -f docker-compose.dev.yml up --build
```

This will start the following services:

- **PostgreSQL**
- **Django Backend**
- **Nginx** (if included in the development setup)

### 4. Running in Production Mode

To deploy the project in production:

```sh
docker-compose -f docker-compose.prod.yml up --build -d
```

### 5. Accessing the Application

- **Django Backend API**: http://localhost:8000
- **Nginx Server**: http://localhost (if configured)

### 6. Managing the Database

To access the PostgreSQL database:

```sh
docker exec -it <postgres_container_id> psql -U postgres -d postgres
```

### 7. Running Migrations

Inside the backend container, run:

```sh
docker exec -it <backend_container_id> python manage.py migrate
```

### 8. Creating a Superuser

To create a Django superuser:

```sh
docker exec -it <backend_container_id> python manage.py createsuperuser
```

### 9. Stopping the Services

To stop the running containers:

```sh
docker-compose -f docker-compose.prod.yml down
```
### 10. Reset all 
1. **Stop and Remove All Containers**
Stop and remove all running containers to ensure no dependencies are active.
    ```sh
    docker stop $(docker ps -aq)
    ```
    ```sh
    docker rm $(docker ps -aq)
    ```
2. **Remove All Images**
Delete all Docker images.
    ```sh
    docker rmi $(docker images -q) -f
    ```
3. **Remove All Volumes**
Remove all Docker volumes.
    ```sh
    docker volume rm $(docker volume ls -q)
    ```
4. **Optional: Prune Everything (if you want a clean slate)**
To remove all unused containers, networks, images, and volumes, you can run the prune command:
    ```sh
    docker system prune -a --volumes -f
    ```

## Data Migration Process

To migrate data from one database to another (e.g., SQLite to MySQL), follow these steps:

### 1. Dump the Data
```sh
python manage.py dumpdata > datadump.json
```

### 2. Configure MySQL in `settings.py`
Modify your `settings.py` file to connect to your MySQL database. Ensure your MySQL server is running and has the correct permissions.

### 3. Apply Migrations
```sh
python manage.py migrate --run-syncdb
```

### 4. Remove ContentType Data
Run the following commands in the Django shell to exclude `ContentType` data:
```sh
python manage.py shell
```
Then, execute:
```python
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
```

### 5. Load the Dumped Data
```sh
python manage.py loaddata datadump.json
```
### 6. Migrate from SQL Dump File
If you have an SQL dump file, you can restore it as follows:
```sh
docker exec -i <mysql_container_id> mysql -u <db_user> -p<db_password> <db_name> < dumpfile.sql
```
Ensure the database is created before running the import command.

---
