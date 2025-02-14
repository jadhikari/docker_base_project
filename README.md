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
### **🚀 CI/CD Pipeline for Django + Nginx + PostgreSQL using GitHub Actions & Docker Compose**
This project uses **GitHub Actions** to automate the deployment of a **Django backend, Nginx, and PostgreSQL** with **Docker Compose**. The deployment process ensures that **new code is automatically built, pushed, and deployed** whenever changes are pushed to the `master` branch.

---

## **📌 CI/CD Workflow Overview**
1. **Push to `master`**: The CI/CD pipeline triggers when new commits are pushed to the `master` branch.
2. **Build & Push Docker Images**:
   - The Django backend image is **built and pushed** to **GitHub Container Registry (GHCR)**.
   - Nginx is managed directly by **Docker Compose** (no manual build).
3. **Deploy to the Server**:
   - The latest changes are **pulled** on the server.
   - **Docker Compose restarts the services**.
   - The database is **migrated**, and static files are **collected**.

---

## **📜 GitHub Actions Workflow**
The CI/CD workflow is defined in `.github/workflows/deploy.yml`:

```yaml
name: Deploy Django with Nginx & PostgreSQL

on:
  push:
    branches:
      - master

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry (GHCR)
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GHCR_PAT }}  # Use Personal Access Token

      - name: Build and Push Backend Image to GHCR
        run: |
          docker build -t ghcr.io/${{ github.repository }}/django-backend:latest -f project_backend/Dockerfile ./project_backend
          docker push ghcr.io/${{ github.repository }}/django-backend:latest

      - name: Deploy on Server
        uses: appleboy/ssh-action@v0.1.10
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /home/ubuntu/docker_base_solar_project
            git pull origin master

            # Stop and remove existing containers
            sudo docker-compose -f docker-compose.prod.yml down

            # Clean up old images
            sudo docker system prune -af

            # Start everything using Docker Compose (Docker will handle pulling if needed)
            sudo docker-compose -f docker-compose.prod.yml up --build -d

            # Wait for services to start
            sleep 10

            # Run Django management commands inside the backend container
            sudo docker exec django-backend-prod pip install -r /app/requirements.txt
            sudo docker exec django-backend-prod python manage.py migrate --noinput
            sudo docker exec django-backend-prod python manage.py collectstatic --noinput

            # Restart Django container to apply updates
            sudo docker restart django-backend-prod
```

---

## **📌 How Docker Compose is Used**
- The CI/CD process **does not manually build Nginx**; instead, **Docker Compose handles it**.
- Docker Compose **pulls images only if they are missing** using:
  ```yaml
  pull_policy: if_not_present
  ```
- Deployment script **removes old images** to free space.

### **Example `docker-compose.prod.yml`**
```yaml
version: '3.8'

services:
  backend:
    image: ghcr.io/${{ github.repository }}/django-backend:latest
    pull_policy: if_not_present  # ✅ Pull only if not available
    restart: always
    env_file: .env.prod
    depends_on:
      - postgres
    command: gunicorn --chdir /app/project_backend --workers 3 --bind 0.0.0.0:8000 project_backend.wsgi:application

  postgres:
    image: postgres:15
    pull_policy: if_not_present  # ✅ Pull only if not available
    restart: always
    env_file: .env.prod
    volumes:
      - postgres-db-prod:/var/lib/postgresql/data

  nginx:
    image: nginx:latest
    restart: always
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media
    depends_on:
      - backend

volumes:
  postgres-db-prod:
    name: solar_project_postgres_data
```

---

## **📌 Environment Variables (Secrets)**
To authenticate and deploy, you must configure the following **GitHub Secrets**:

| Secret Name        | Purpose |
|--------------------|---------|
| `GHCR_PAT`        | GitHub Personal Access Token (for pushing images to GHCR) |
| `SERVER_IP`       | Public IP of the server |
| `SERVER_USER`     | SSH username (e.g., `ubuntu`) |
| `SSH_PRIVATE_KEY` | SSH private key for connecting to the server |

---

## **🚀 How to Deploy Manually (if needed)**
If GitHub Actions fails or you need to manually redeploy, **run these commands on the server**:

```bash
cd /home/ubuntu/docker_base_solar_project
git pull origin master

sudo docker-compose -f docker-compose.prod.yml down
sudo docker system prune -af  # Free up space
sudo docker-compose -f docker-compose.prod.yml up --build -d
```

If you want to **force an image update**, manually pull the latest images:

```bash
sudo docker pull ghcr.io/your-github-org/docker_base_solar_project/django-backend:latest
sudo docker-compose -f docker-compose.prod.yml up --build -d
```

---

## **💡 Key Features of This CI/CD Pipeline**
✔ **Fully Automated Deployment** → Push to `master` triggers automatic deployment.  
✔ **Uses GitHub Container Registry (GHCR)** → Secure and integrated with GitHub.  
✔ **Docker Compose Handles Everything** → No manual builds for Nginx.  
✔ **Pulls Only When Necessary** → Prevents unnecessary image downloads (`pull_policy: if_not_present`).  
✔ **Runs Django Migrations & Static Collection** → Ensures the database and frontend assets are up-to-date.  

---

### **📌 Next Steps**
- ✅ **Ensure GitHub Secrets are correctly set up.**
- ✅ **Push code to `master` to trigger automatic deployment.**
- ✅ **Monitor logs using:**
  ```bash
  docker logs django-backend-prod -f
  ```

