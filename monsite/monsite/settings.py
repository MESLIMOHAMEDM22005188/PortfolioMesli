
"""
monsite/settings.py
Configuration Django pour PortfolioMeslii.
Compatible avec le développement local, Render et AlwaysData.
"""

import logging
import os
from pathlib import Path

import dj_database_url
from decouple import config


# ==================================================
# CONFIGURATION GÉNÉRALE
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


# ==================================================
# SÉCURITÉ
# ==================================================

DEBUG = config("DEBUG", default=False, cast=bool)

SECRET_KEY = config("SECRET_KEY", default="")

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-local-development-only-key"
        logger.warning(
            "Clé secrète temporaire utilisée en développement. "
            "Ne jamais l'utiliser en production."
        )
    else:
        raise RuntimeError(
            "SECRET_KEY doit être définie dans les variables d'environnement."
        )

ALLOWED_HOSTS = [
    host.strip()
    for host in config("ALLOWED_HOSTS", default="").split(",")
    if host.strip()
]

if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]

ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))

if not DEBUG and not ALLOWED_HOSTS:
    raise RuntimeError(
        "ALLOWED_HOSTS doit être configuré en production."
    )

CSRF_TRUSTED_ORIGINS = [
    origin.strip().rstrip("/")
    for origin in config("CSRF_TRUSTED_ORIGINS", default="").split(",")
    if origin.strip()
]


# ==================================================
# BASE DE DONNÉES
# ==================================================

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
elif DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    raise RuntimeError(
        "DATABASE_URL doit être configurée en production."
    )


# ==================================================
# APPLICATIONS DJANGO
# ==================================================

INSTALLED_APPS = [
    # Applications du projet
    "users",
    "tickets.apps.TicketsConfig",
    "portfolio",
    "widget_tweaks",

    # Applications Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Extensions
    "django_extensions",
]


# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==================================================
# URLS ET SERVEUR
# ==================================================

ROOT_URLCONF = "monsite.urls"

WSGI_APPLICATION = "monsite.wsgi.application"


# ==================================================
# TEMPLATES
# ==================================================

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


# ==================================================
# FICHIERS STATIQUES
# ==================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}


# ==================================================
# AUTHENTIFICATION
# ==================================================

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "/tickets/"
LOGIN_REDIRECT_URL = "/tickets/list/"
LOGOUT_REDIRECT_URL = "/"


# ==================================================
# E-MAILS
# ==================================================

EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)

EMAIL_USE_TLS = config(
    "EMAIL_USE_TLS",
    cast=bool,
    default=True,
)

EMAIL_USE_SSL = config(
    "EMAIL_USE_SSL",
    cast=bool,
    default=False,
)

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default="webmaster@localhost",
)


# ==================================================
# INTERNATIONALISATION
# ==================================================

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"

USE_I18N = True
USE_TZ = True


# ==================================================
# PROTECTIONS HTTP ET COOKIES
# ==================================================

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False

X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

if not DEBUG:
    SECURE_SSL_REDIRECT = config(
        "SECURE_SSL_REDIRECT",
        default=True,
        cast=bool,
    )

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = config(
        "SECURE_HSTS_SECONDS",
        default=3600,
        cast=int,
    )

    # Activer ces options uniquement après validation
    # de la configuration HTTPS de tous les sous-domaines.
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

    # À activer uniquement derrière un proxy de confiance
    # qui transmet correctement le protocole HTTPS.
    if config(
        "SECURE_PROXY_SSL_HEADER_ENABLED",
        default=False,
        cast=bool,
    ):
        SECURE_PROXY_SSL_HEADER = (
            "HTTP_X_FORWARDED_PROTO",
            "https",
        )


SITE_ID = 1


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
