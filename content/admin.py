"""Register every content table in Django Admin so content can be added there."""
from django.contrib import admin

from .models import FooterLink, NavItem, NewsItem, PageSection, SiteSettings, Slide, SocialLink, Stat


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "email", "phone")

    def has_add_permission(self, request):
        # Allow only one settings row
        return not SiteSettings.objects.exists()


class NavChildInline(admin.TabularInline):
    # Lets the admin add dropdown links directly inside their parent menu item
    model = NavItem
    fk_name = "parent"
    extra = 1
    fields = ("title", "url", "order", "is_active")


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "parent", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("location", "parent")
    inlines = [NavChildInline]


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("__str__", "media_type", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "section_type", "background", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("section_type",)


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("value", "suffix", "label", "order")
    list_editable = ("order",)


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date", "is_published")
    list_editable = ("is_published",)
    search_fields = ("title", "category")


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "order")
    list_editable = ("order",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "order")
    list_editable = ("order",)
