#Use the offical Pythin runtime image
FROM python:3.13-slim AS builder

#Create the app directory
RUN mkdir /app

#Set the working directory inside the container
WORKDIR /app

#Set environment variables
#Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Pythin from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

#Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


#Production Stage
FROM python:3.13-slim


RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

#Copy the python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

#Set the working directory
WORKDIR /app

# Set application Code
COPY --chown=appuser:appuser . .

# Set environment variable to optimize python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Switch to non-root user
USER appuser

#Expose the django port
EXPOSE 8000

# RUN python manage.py collectstatic --noinput

#Run Django's development server
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "my_docker_django_app.wsgi:application"]


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
