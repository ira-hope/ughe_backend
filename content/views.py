"""REST API endpoints used by the Next.js frontend."""
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FooterLink, NavItem, NewsItem, PageSection, SiteSettings, Slide, SocialLink, Stat
from . import serializers as s


class LoginView(APIView):
    """POST username + password, get back a token if the credentials are correct."""

    # Anyone can reach the login endpoint
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        user = authenticate(
            username=request.data.get("username", ""),
            password=request.data.get("password", ""),
        )
        if user is None:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Create (or reuse) the user's login token
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})


class LogoutView(APIView):
    """Delete the user's token so it can no longer be used."""

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Logged out."})


class SiteInfoView(APIView):
    """Public site info (name + logo) so the login page can show the logo."""

    permission_classes = [AllowAny]

    def get(self, request):
        settings = SiteSettings.objects.first()
        if settings is None:
            return Response({})
        return Response(s.SiteSettingsSerializer(settings, context={"request": request}).data)


class HomeView(APIView):
    """Everything the home page needs, in one request (login token required)."""

    def get(self, request):
        ctx = {"request": request}
        settings = SiteSettings.objects.first()
        # Top-level menu items only, their dropdown children are nested inside
        main_menu = NavItem.objects.filter(location=NavItem.MAIN_MENU, parent=None, is_active=True)
        top_buttons = NavItem.objects.filter(location=NavItem.TOP_BUTTON, parent=None, is_active=True)
        return Response({
            "site": s.SiteSettingsSerializer(settings, context=ctx).data if settings else {},
            "main_menu": s.NavItemSerializer(main_menu, many=True).data,
            "top_buttons": s.NavItemSerializer(top_buttons, many=True).data,
            "slides": s.SlideSerializer(Slide.objects.filter(is_active=True), many=True, context=ctx).data,
            "sections": s.PageSectionSerializer(
                PageSection.objects.filter(is_active=True), many=True, context=ctx
            ).data,
            "stats": s.StatSerializer(Stat.objects.all(), many=True).data,
            "news": s.NewsItemSerializer(
                NewsItem.objects.filter(is_published=True)[:6], many=True, context=ctx
            ).data,
            "footer_links": s.FooterLinkSerializer(FooterLink.objects.all(), many=True).data,
            "social_links": s.SocialLinkSerializer(SocialLink.objects.all(), many=True).data,
        })
