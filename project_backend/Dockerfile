# Base image for both environments
FROM python:3.10.12-slim AS base

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y apt-utils && apt-get install -y vim nano && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base AS development

# Additional tools for development
RUN pip install --no-cache-dir debugpy

# Expose port for development
EXPOSE 8000

# Command to run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base AS production

# Copy project files (for production only)
COPY . .

# Expose port for production
EXPOSE 8000

# Command to run the application in production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "my_docker_django_app.wsgi:application"]

