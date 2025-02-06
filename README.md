# PostgreSQL database configuration for local development
POSTGRES_DB=your_local_database_name
POSTGRES_USER=your_local_database_user
POSTGRES_PASSWORD=your_local_database_password
POSTGRES_HOST=postgres-db
POSTGRES_PORT=5432


# Database Configuration (Development)
POSTGRES_DB=local_database_name
POSTGRES_USER=local_database_user
POSTGRES_PASSWORD=local_database_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Django Configuration
DJANGO_SECRET_KEY=local_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# React API URL
REACT_APP_API_URL=http://localhost:8000/api/


# # Database Configuration (Production)
# POSTGRES_DB=prod_database_name
# POSTGRES_USER=prod_database_user
# POSTGRES_PASSWORD=prod_database_password
# POSTGRES_HOST=db
# POSTGRES_PORT=5432

# # Django Configuration
# DJANGO_SECRET_KEY=production_secret_key
# DJANGO_DEBUG=False
# DJANGO_ALLOWED_HOSTS=your_domain_or_ip

# # React API URL
# REACT_APP_API_URL=https://your_domain_or_ip/api/


pg_conn = psycopg2.connect(
    host="172.24.0.2",
    database="dev_database_name",
    user="dev_database_user",
    password="6tEmi05PGv6PGW",
    port=5432
)


docker-compose -f docker-compose.dev.yml  down --rm


1. **Stop and Remove All Containers**
Stop and remove all running containers to ensure no dependencies are active.
 docker stop $(docker ps -aq)
 docker rm $(docker ps -aq)
2. **Remove All Images**
Delete all Docker images.
 docker rmi $(docker images -q) -f
3. **Remove All Volumes**
Remove all Docker volumes.
 docker volume rm $(docker volume ls -q)
4. **Optional: Prune Everything (if you want a clean slate)**
To remove all unused containers, networks, images, and volumes, you can run the prune command:
 docker system prune -a --volumes -f
**Warning**: This command will remove **everything**, including data volumes


my formula is

python manage.py dumpdata > datadump.json
Change settings.py to your mysql
Make sure you can connect on your mysql (permissions,etc)
python manage.py migrate --run-syncdb
Exclude contentype data with this snippet in shell

python manage.py shell

from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()

python manage.py loaddata datadump.json





psql -U dev_database_user -d dev_database_name


.env.dev
# Database Configuration (Development)
POSTGRES_USER=dev_database_user
POSTGRES_PASSWORD=6tEmi05PGv6PGW
POSTGRES_DB=dev_database_name
POSTGRES_HOST=postgres-db-dev
POSTGRES_PORT=5432

# Django Configuration
DJANGO_SECRET_KEY='django-insecure-#q2z3g*ro$@u9z(nry5!z^$4=z6l9v(6r(d3t=bab3@70$r$t!'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# React API URL
REACT_APP_BASE_URL=http://127.0.0.1:8000/api



