from django.apps import AppConfig


class ContentConfig(AppConfig):
    # App that stores all dynamic website content
    default_auto_field = "django.db.models.BigAutoField"
    name = "content"
    verbose_name = "Website Content"
