"""
monsite/settings.py
Configuration compatible avec le développement local et Render.
"""

import logging
import os
from pathlib import Path

import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# Logging
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# -----------------------
# Environment and security
# -----------------------
IS_RENDER = "RENDER" in os.environ

# Keep the existing fallback for backward compatibility so a deployment
# cannot fail solely because the Render environment variable has not yet
# been configured. Configure SECRET_KEY in Render before treating the
# deployment as production-ready.
SECRET_KEY = config("SECRET_KEY", default="dev-secret")

# Render should never run with Django debug pages enabled. Locally, DEBUG
# remains configurable through .env and defaults to True.
if IS_RENDER:
    DEBUG = False
else:
    DEBUG = config("DEBUG", cast=bool, default=True)

if not DEBUG and SECRET_KEY == "dev-secret":
    logger.warning(
        "SECRET_KEY is using the development fallback. Configure a unique "
        "SECRET_KEY in the production environment before deployment."
    )

ALLOWED_HOSTS = [
    host.strip()
    for host in config("ALLOWED_HOSTS", default="").split(",")
    if host.strip()
]

# Render sets this variable automatically for web services.
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

if DEBUG:
    for host in ("127.0.0.1", "localhost"):
        if host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(host)

# Preserve configured trusted origins, then allow the HTTPS origins for
# explicitly allowed hosts. This also covers Render's generated hostname.
CSRF_TRUSTED_ORIGINS = [
    origin.strip().rstrip("/")
    for origin in config("CSRF_TRUSTED_ORIGINS", default="").split(",")
    if origin.strip()
]
for host in ALLOWED_HOSTS:
    if host and not host.startswith("http") and not host.startswith(".") and host != "*":
        origin = f"https://{host}"
        if origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(origin)

# -----------------------
# Database
# -----------------------
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -----------------------
# Apps
# -----------------------
INSTALLED_APPS = [
    "users",
    "tickets.apps.TicketsConfig",
    "portfolio",
    "widget_tweaks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_extensions",
]

# -----------------------
# Middleware
# -----------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "portfolio.middleware.LanguageSwitcherMiddleware",
]

ROOT_URLCONF = "monsite.urls"

# -----------------------
# Templates
# -----------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "monsite.wsgi.application"

# -----------------------
# Static files
# -----------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Only add the project-level static directory if it actually exists.
# Django will still discover static directories inside installed apps.
STATIC_SOURCE_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [STATIC_SOURCE_DIR] if STATIC_SOURCE_DIR.is_dir() else []

# Django 5.1+ uses STORAGES; STATICFILES_STORAGE has been removed.
# Use WhiteNoise compression without a strict manifest so missing legacy
# references do not make the deployment's collectstatic step fail.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# -----------------------
# Auth config
# -----------------------
AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/tickets/"
LOGIN_REDIRECT_URL = "/tickets/list/"

# -----------------------
# Email
# -----------------------
EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="webmaster@localhost")

# -----------------------
# Internationalization
# -----------------------
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# -----------------------
# Production security
# -----------------------
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Render terminates TLS at its proxy. Trust the HTTPS indicator from
    # that proxy; Render already redirects external HTTP requests to HTTPS.
    if IS_RENDER:
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
        SECURE_SSL_REDIRECT = False
        # W008 is not applicable because Render performs the redirect
        # before the request reaches Django.
        SILENCED_SYSTEM_CHECKS = ["security.W008"]
    else:
        # For other production hosts, HTTPS redirection is enabled by
        # default but can be configured for hosts with their own proxy.
        SECURE_SSL_REDIRECT = config(
            "SECURE_SSL_REDIRECT",
            cast=bool,
            default=True,
        )

    # Start with a short HSTS duration. Do not force subdomains or preload.
    SECURE_HSTS_SECONDS = config(
        "SECURE_HSTS_SECONDS",
        cast=int,
        default=3600,
    )
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
