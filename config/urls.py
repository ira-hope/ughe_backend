"""Main URL routes of the backend."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Customise the Django Admin titles
admin.site.site_header = "UGHE Test Web App - Admin"
admin.site.site_title = "UGHE Admin"
admin.site.index_title = "Manage website content"

urlpatterns = [
    # Django Admin where all the website content is added
    path("admin/", admin.site.urls),
    # REST API consumed by the Next.js frontend
    path("api/", include("content.urls")),
]

# Serve uploaded images/videos while developing locally
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
