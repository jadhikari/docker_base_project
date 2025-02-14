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

