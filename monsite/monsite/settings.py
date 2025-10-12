"""
monsite/settings.py
Version propre : dev-safe + ready-for-prod (uses python-decouple)
Ne jamais committer un .env contenant des secrets.
"""

import os
from pathlib import Path
from decouple import config

# Optional MySQL shim
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # pymysql non nécessaire si on utilise sqlite en dev
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# Security & flags
# -----------------------
SECRET_KEY = config('SECRET_KEY', default='dev-temporary-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS can be provided as CSV in env: "yourapp.onrender.com,www.example.com"
_raw_hosts = config('ALLOWED_HOSTS', default='')
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(',') if h.strip()] if _raw_hosts else []

# -----------------------
# Installed apps
# -----------------------
INSTALLED_APPS = [
    # project apps
    'users',
    'tickets.apps.TicketsConfig',
    'portfolio',

    # django contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django_extensions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # third party
    'widget_tweaks',
]

SITE_ID = 1

# -----------------------
# Middleware
# -----------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serve static files in prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monsite.urls'

# -----------------------
# Templates
# -----------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -----------------------
# Static files
# -----------------------
# Candidate path used previously in the project; include only if present
_candidate_static = BASE_DIR / "monsite" / "tickets" / "static"
STATICFILES_DIRS = [ _candidate_static ] if _candidate_static.exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# WhiteNoise storage for compressed + manifest (cache busting)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WSGI_APPLICATION = 'monsite.wsgi.application'

# -----------------------
# DATABASE (priority):
# 1) DATABASE_URL env (postgres/mysql)
# 2) MySQL via DB_NAME / DB_USER / DB_PASSWORD
# 3) fallback sqlite for dev
# -----------------------
DATABASE_URL = os.environ.get('DATABASE_URL') or config('DATABASE_URL', default='')

if DATABASE_URL:
    try:
        import dj_database_url
    except ImportError:
        raise RuntimeError("dj-database-url is required when using DATABASE_URL. pip install dj-database-url")
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DB_NAME = config('DB_NAME', default='')
    if DB_NAME:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME':   DB_NAME,
                'USER':   config('DB_USER', default=''),
                'PASSWORD': config('DB_PASSWORD', default=''),
                'HOST':   config('DB_HOST', default='127.0.0.1'),
                'PORT':   config('DB_PORT', cast=int, default=3306),
                'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# -----------------------
# Email (safe defaults)
# -----------------------
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

# -----------------------
# Auth & misc
# -----------------------
LOGIN_URL = '/tickets/'
LOGIN_REDIRECT_URL = '/tickets/list/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# -----------------------
# Security for production
# -----------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# -----------------------
# Default primary key
# -----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
