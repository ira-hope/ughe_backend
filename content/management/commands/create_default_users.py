"""Create the predefined login accounts (run automatically when the container starts)."""
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the predefined frontend user and the Django Admin superuser."

    def handle(self, *args, **options):
        # Predefined credentials, can be changed through environment variables
        app_username = os.environ.get("APP_USERNAME", "ughe")
        app_password = os.environ.get("APP_PASSWORD", "Ughe@2026")
        admin_username = os.environ.get("ADMIN_USERNAME", "admin")
        admin_password = os.environ.get("ADMIN_PASSWORD", "Admin@2026")

        # Normal user who logs in on the Next.js frontend
        if not User.objects.filter(username=app_username).exists():
            User.objects.create_user(username=app_username, password=app_password)
            self.stdout.write(f"Created frontend user '{app_username}'")

        # Superuser who adds content in Django Admin (can also log in on the frontend)
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username, email="admin@example.com", password=admin_password
            )
            self.stdout.write(f"Created admin user '{admin_username}'")
