"""
Production-style server entrypoint using waitress instead of Django's
built-in `runserver` (which is explicitly not meant for continuous/production
use). Static files are still served correctly - urls.py serves STATIC_ROOT
directly regardless of which server is running this.
"""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kensova_core.settings')

from waitress import serve
from kensova_core.wsgi import application

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=8009, threads=8)
