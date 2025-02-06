from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from `.env.prod`
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Debug Mode (Ensures value is parsed correctly)
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("true", "1")

# Allowed Hosts
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(",")

# CORS and CSRF Trusted Origins
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
# Tell Django that requests are forwarded from a proxy (Nginx)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Secret Key
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")

# Installed Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "user",
    "core",
]

# Middleware settings
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Django Rest Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.TokenAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# URL and WSGI settings
ROOT_URLCONF = "project_backend.urls"
WSGI_APPLICATION = "project_backend.wsgi.application"

# Templates settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Spectacular API Documentation settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Solar API",
    "DESCRIPTION": "API documentation for Solar Project",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
}

# Database settings (Loaded from `.env.prod`)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "solar_db"),
        "USER": os.getenv("POSTGRES_USER", "solar_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "solar_password"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static and media file settings
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Authentication settings
AUTH_USER_MODEL = "user.User"
LOGIN_REDIRECT_URL = "/solar-api/admin/"
LOGOUT_REDIRECT_URL = "/solar-api/admin/login/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security headers (for production)
if not DEBUG:
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
