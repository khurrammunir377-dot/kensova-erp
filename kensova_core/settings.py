import os
import dj_database_url
from pathlib import Path
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY is generated once on first run and stored in a local file that
# is never shipped/shared with the project (unlike a hardcoded key in this
# .py file, which would let anyone who has this folder forge session
# cookies). Delete the file to rotate the key (this logs everyone out).
_secret_key_file = BASE_DIR / '.secret_key'
if _secret_key_file.exists():
    SECRET_KEY = _secret_key_file.read_text().strip()
else:
    SECRET_KEY = get_random_secret_key()
    _secret_key_file.write_text(SECRET_KEY)

# Was True - left the app leaking full stack traces, settings, and source
# paths to anyone who could reach an error page (and since the server binds
# to 0.0.0.0, that's everyone on the same network, not just this PC).
DEBUG = False

# '*' is kept (rather than a fixed IP) because the app needs to keep working
# if this PC's LAN IP changes. DEBUG=False is what actually neutralizes the
# risk that made '*' dangerous - Host-header tricks mostly matter for pages
# that leak internals or use the Host header in links/emails, neither of
# which this app does.
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kensova_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'store_app' / 'templates'],
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

WSGI_APPLICATION = 'kensova_core.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Was []: any password (including a 1-character one) was accepted for any
# staff account. This restores Django's normal minimum-strength checks.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dubai'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
# Needed now that DEBUG=False - runserver only auto-serves static files via
# the app-static-folder finder when DEBUG=True. collectstatic (run by the
# launcher .bat each start) copies everything here, and urls.py serves this
# folder directly so styling/scripts keep working with DEBUG off.
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Auto-logout after 8 hours of inactivity, or when the Edge app window is
# closed - reduces the risk of a staff member's session being left open
# indefinitely on a shared PC.
SESSION_COOKIE_AGE = 28800
SESSION_EXPIRE_AT_BROWSER_CLOSE = True