"""WSGI entry point used to run the Django project."""
import os

from django.core.wsgi import get_wsgi_application

# Point Django to our project settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
