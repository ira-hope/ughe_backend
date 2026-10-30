"""Convert database rows into JSON for the REST API."""
from rest_framework import serializers

from .models import FooterLink, NavItem, NewsItem, PageSection, SiteSettings, Slide, SocialLink, Stat


def file_or_url(request, uploaded_file, url):
    # Use the uploaded file if there is one, otherwise use the online link
    if uploaded_file:
        return request.build_absolute_uri(uploaded_file.url)
    return url or ""


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    footer_logo = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        exclude = ("id", "logo_url", "footer_logo_url")

    def get_logo(self, obj):
        return file_or_url(self.context["request"], obj.logo, obj.logo_url)

    def get_footer_logo(self, obj):
        return file_or_url(self.context["request"], obj.footer_logo, obj.footer_logo_url)


class NavItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = NavItem
        fields = ("id", "title", "url", "children")

    def get_children(self, obj):
        # Only send active dropdown items
        return NavItemSerializer(obj.children.filter(is_active=True), many=True).data


class SlideSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()

    class Meta:
        model = Slide
        fields = ("id", "title", "subtitle", "button_text", "button_url", "media_type", "media")

    def get_media(self, obj):
        return file_or_url(self.context["request"], obj.media_file, obj.media_url)


class PageSectionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PageSection
        fields = (
            "id", "section_type", "title", "body", "button_text", "button_url",
            "image", "video_url", "image_position", "background",
        )

    def get_image(self, obj):
        return file_or_url(self.context["request"], obj.image, obj.image_url)


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ("id", "value", "suffix", "label")


class NewsItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewsItem
        fields = ("id", "title", "category", "date", "image", "link")

    def get_image(self, obj):
        return file_or_url(self.context["request"], obj.image, obj.image_url)


class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = ("id", "title", "url")


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ("id", "platform", "url")
