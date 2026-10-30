"""API routes, all prefixed with /api/ (see config/urls.py)."""
from django.urls import path

from .views import HomeView, LoginView, LogoutView, SiteInfoView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("site/", SiteInfoView.as_view(), name="site-info"),
    path("home/", HomeView.as_view(), name="home"),
]
