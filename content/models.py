"""Database tables for every piece of content shown on the Next.js home page."""
from django.db import models


class SiteSettings(models.Model):
    """General site info: logos, contacts and footer text (only the first row is used)."""

    site_name = models.CharField(max_length=150, default="UGHE Test Web App")
    # Each image can be uploaded OR given as an online link (upload wins if both exist)
    logo = models.ImageField(upload_to="site/", blank=True)
    logo_url = models.URLField(blank=True)
    footer_logo = models.ImageField(upload_to="site/", blank=True)
    footer_logo_url = models.URLField(blank=True)
    footer_tagline = models.TextField(blank=True)
    campus_address = models.CharField(max_length=255, blank=True)
    office_hours = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    kigali_office = models.CharField(max_length=255, blank=True)
    copyright_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.site_name


class NavItem(models.Model):
    """A link in the header: main menu item, its dropdown children, or a top button."""

    MAIN_MENU = "main"
    TOP_BUTTON = "top"
    LOCATION_CHOICES = [(MAIN_MENU, "Main menu"), (TOP_BUTTON, "Top bar button")]

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=500, blank=True, default="#")
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default=MAIN_MENU)
    # Pick a parent to make this item appear inside that item's dropdown
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Navigation item"

    def __str__(self):
        return f"{self.parent.title} > {self.title}" if self.parent else self.title


class Slide(models.Model):
    """One item of the hero slideshow, it can be an image or a video."""

    IMAGE = "image"
    VIDEO = "video"
    MEDIA_CHOICES = [(IMAGE, "Image"), (VIDEO, "Video (MP4 file/link or YouTube link)")]

    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    button_text = models.CharField(max_length=60, blank=True)
    button_url = models.CharField(max_length=500, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default=IMAGE)
    # Upload a file OR paste a link to an online image/video
    media_file = models.FileField(upload_to="slides/", blank=True)
    media_url = models.URLField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or f"Slide {self.pk}"


class PageSection(models.Model):
    """A block of the home page; its type decides how the frontend draws it."""

    STATS = "stats"
    FEATURE = "feature"
    NEWS = "news"
    VIDEO = "video"
    TYPE_CHOICES = [
        (STATS, "Facts & stats (uses the Stat items)"),
        (FEATURE, "Text + image block"),
        (NEWS, "News list (uses the News items)"),
        (VIDEO, "Video block"),
    ]
    BG_CHOICES = [("white", "White"), ("light", "Light grey"), ("red", "UGHE red"), ("dark", "Dark")]
    POSITION_CHOICES = [("left", "Image on the left"), ("right", "Image on the right")]

    section_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=FEATURE)
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    button_text = models.CharField(max_length=60, blank=True)
    button_url = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to="sections/", blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    video_url = models.URLField(max_length=500, blank=True)
    image_position = models.CharField(max_length=5, choices=POSITION_CHOICES, default="right")
    background = models.CharField(max_length=10, choices=BG_CHOICES, default="white")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Home page section"

    def __str__(self):
        return f"{self.title} ({self.get_section_type_display()})"


class Stat(models.Model):
    """A number shown in the 'Facts & Stats' section."""

    value = models.CharField(max_length=30, help_text="Example: 1,260 or 4")
    suffix = models.CharField(max_length=10, blank=True, help_text="Example: + or TH")
    label = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value}{self.suffix} - {self.label}"


class NewsItem(models.Model):
    """A news card shown in the 'News & Updates' section."""

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    image = models.ImageField(upload_to="news/", blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    link = models.URLField(max_length=500, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        # Newest news first
        ordering = ["-date", "-id"]
        verbose_name = "News item"

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    """A quick link shown at the bottom of the footer."""

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class SocialLink(models.Model):
    """A social media icon link shown in the footer."""

    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("x", "X (Twitter)"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("youtube", "YouTube"),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.get_platform_display()
