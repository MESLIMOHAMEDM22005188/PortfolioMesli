"""
monsite/settings.py
Version prod/dev sûre (AlwaysData, Render, etc.) – lit la config depuis l'environnement.
"""

import os
from pathlib import Path
from decouple import config
from django.conf import settings

# Optional MySQL shim (ok si non utilisé)
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# Security & flags
# -----------------------
SECRET_KEY = config('SECRET_KEY', default='dev-temporary-secret-key')
DEBUG = config('DEBUG', default=False, cast=bool)


def _csv(name: str, default: str = ""):
    """Lit une variable d'env CSV et la transforme en liste."""
    raw = config(name, default=default)
    return [x.strip() for x in raw.split(",") if x.strip()]


ALLOWED_HOSTS = _csv('ALLOWED_HOSTS')
if DEBUG:
    # Permet le test en local sans DisallowedHost
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

CSRF_TRUSTED_ORIGINS = _csv('CSRF_TRUSTED_ORIGINS')
if not CSRF_TRUSTED_ORIGINS and ALLOWED_HOSTS:
    # Autorise HTTPS sur les hosts déclarés
    CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if not h.startswith('http')]

# Toujours correct derrière un proxy (Render / AlwaysData)
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SITE_ID = config('SITE_ID', default=1, cast=int)

# Si on est en prod: ALLOWED_HOSTS doit être rempli
if not DEBUG and not ALLOWED_HOSTS:
    raise RuntimeError("ALLOWED_HOSTS must be set in production (env ALLOWED_HOSTS)")

# -----------------------
# Installed apps
# -----------------------
INSTALLED_APPS = [
    # Project apps
    'users',
    'tickets.apps.TicketsConfig',
    'portfolio',
    'sslserver',

    # Django contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Dev / utils
    'django_extensions',  # OK aussi en prod, mais peut être retiré
    'widget_tweaks',
]

# -----------------------
# Middleware
# -----------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # sert les statiques efficacement
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
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'monsite.wsgi.application'

# -----------------------
# Static files
# -----------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
_global_static = BASE_DIR / 'static'
if _global_static.exists():
    STATICFILES_DIRS = [_global_static]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# -----------------------
# Database configuration
# -----------------------
DATABASE_URL = os.environ.get('DATABASE_URL') or config('DATABASE_URL', default='')

if DATABASE_URL:
    try:
        import dj_database_url
    except ImportError:
        raise RuntimeError("dj-database-url is required when using DATABASE_URL. Install with: pip install dj-database-url")
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DB_NAME = config('DB_NAME', default='')
    if DB_NAME:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': DB_NAME,
                'USER': config('DB_USER', default=''),
                'PASSWORD': config('DB_PASSWORD', default=''),
                'HOST': config('DB_HOST', default='127.0.0.1'),
                'PORT': config('DB_PORT', cast=int, default=3306),
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

DJANGO_SETTINGS_MODULE = settings


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# -----------------------
# Production security
# -----------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'same-origin'

else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
if DEBUG:
    import warnings
    from django.http import HttpResponseRedirect

    class ForceHttpMiddleware:
        """Empêche toute tentative d'accès HTTPS en local"""
        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            if request.is_secure():
                url = request.build_absolute_uri(request.get_full_path())
                url = url.replace("https://", "http://")
                return HttpResponseRedirect(url)
            return self.get_response(request)

    MIDDLEWARE.insert(0, 'monsite.settings.ForceHttpMiddleware')
# -----------------------
# Logging
# -----------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "django.security.DisallowedHost": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}

# -----------------------
# Default primary key
# -----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
