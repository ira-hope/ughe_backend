"""Fill the database with sample content taken from https://ughe.org.

This is only starter data saved INTO the database; everything can then be
edited, removed or added in Django Admin. Nothing is hardcoded in the frontend.
"""
from datetime import date

from django.core.management.base import BaseCommand

from content.models import FooterLink, NavItem, NewsItem, PageSection, SiteSettings, Slide, SocialLink, Stat

# Base folder of the images on the UGHE website
UP = "https://ughe.org/wp-content/uploads"


class Command(BaseCommand):
    help = "Load sample UGHE content (skipped if content already exists, use --force to reload)."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Delete existing content and reload it")

    def handle(self, *args, **options):
        # Do not overwrite content that was already added in Django Admin
        if SiteSettings.objects.exists() and not options["force"]:
            self.stdout.write("Content already exists, skipping seed.")
            return

        # Clear old content when --force is used
        for model in (SiteSettings, NavItem, Slide, PageSection, Stat, NewsItem, FooterLink, SocialLink):
            model.objects.all().delete()

        self.seed_site()
        self.seed_menu()
        self.seed_slides()
        self.seed_sections()
        self.seed_news()
        self.seed_footer()
        self.stdout.write(self.style.SUCCESS("Sample UGHE content loaded."))

    def seed_site(self):
        SiteSettings.objects.create(
            site_name="UGHE Test Web App",
            logo_url=f"{UP}/2026/04/UGHE-H.png",
            footer_logo_url=f"{UP}/2026/04/UGHE-H-White.png",
            footer_tagline="We're on a mission to radically change the way health care is delivered around the world.",
            campus_address="Butaro, Burera, Rwanda",
            office_hours="8:00 a.m. – 5:00 p.m.",
            phone="+250 786 405 072",
            email="info@ughe.org",
            kigali_office="KG 7 Ave, Kigali Heights, 5th Floor, East Wing. P.O. Box 6955",
            copyright_text="© 2026 UGHE. All Rights Reserved",
        )

    def seed_menu(self):
        # Top bar buttons
        for i, (title, url) in enumerate([
            ("Apply", "https://ughe.org/admission/"),
            ("Get Involved", "https://ughe.org/get-involved/"),
            ("Meet the Team", "https://ughe.org/leadership/"),
        ]):
            NavItem.objects.create(title=title, url=url, location=NavItem.TOP_BUTTON, order=i)

        # Main menu items and their dropdown children
        menu = [
            ("About Us", "https://ughe.org/about", [
                ("Our Story", "https://ughe.org/about"),
                ("Leadership", "https://ughe.org/leadership/"),
                ("University Medalists", "https://ughe.org/university-medalists/"),
            ]),
            ("Academics", "https://ughe.org/academics/", [
                ("School of Medicine", "https://ughe.org/school-of-medicine/"),
                ("Graduate Programs", "https://ughe.org/academics/"),
                ("Professional and Executive Programs", "https://ughe.org/professional-and-executive-education-programs/"),
            ]),
            ("Research", "https://ughe.org/research/", []),
            ("Centres and Institutes", "#", [
                ("Centre for One Health", "https://ughe.org/"),
                ("Centre for Gender Equity", "https://ughe.org/"),
                ("Centre for Equity in Global Surgery", "https://ughe.org/"),
            ]),
            ("Admissions", "https://ughe.org/admission/", [
                ("Apply to UGHE", "https://ughe.org/admission/"),
                ("Tuition, Fees & Financial Aid", "https://ughe.org/tuition-fees-financial-aid/"),
                ("I've Been Admitted", "https://ughe.org/ive-been-admitted/"),
            ]),
            ("News and Events", "https://ughe.org/news/", [
                ("UGHE Stories", "https://ughe.org/news/"),
                ("Press Releases", "https://ughe.org/press-releases/"),
                ("Newsletters", "https://ughe.org/newsletters/"),
            ]),
        ]
        for i, (title, url, children) in enumerate(menu):
            parent = NavItem.objects.create(title=title, url=url, order=i)
            for j, (c_title, c_url) in enumerate(children):
                NavItem.objects.create(title=c_title, url=c_url, parent=parent, order=j)

    def seed_slides(self):
        # Mix of images and a video to show the slideshow supports both
        Slide.objects.create(
            title="10 Years of Impact",
            subtitle="The late Dr. Paul Farmer envisioned a healthier, more equitable world. "
                     "Today, his legacy thrives as we celebrate ten years of impact.",
            button_text="Learn More", button_url="https://ughe.org/ughe-turns-10/",
            media_type=Slide.IMAGE, media_url=f"{UP}/2026/05/55269586520_bb7163c180_5k-scaled.jpg", order=0,
        )
        Slide.objects.create(
            title="Experience Our Impact",
            subtitle="From classrooms to communities, UGHE is transforming healthcare across Africa and beyond.",
            button_text="Watch on YouTube", button_url="https://www.youtube.com/watch?v=M2l7sCuOnHo",
            media_type=Slide.VIDEO, media_url="https://www.youtube.com/watch?v=M2l7sCuOnHo", order=1,
        )
        Slide.objects.create(
            title="Study at UGHE",
            subtitle="A next-generation university training the next generation of global health leaders.",
            button_text="About Admission", button_url="https://ughe.org/admission/",
            media_type=Slide.IMAGE, media_url=f"{UP}/2026/07/Tumenye-Kaminuza.jpg", order=2,
        )

    def seed_sections(self):
        PageSection.objects.create(
            section_type=PageSection.STATS, title="Facts & Stats", background="white", order=0,
        )
        for i, (value, suffix, label) in enumerate([
            ("128", "", "Trained community members through UGHE entrepreneurship initiatives"),
            ("1,260", "", "Community members employed for Campus projects"),
            ("677", "", "Leaders across 61 countries trained in our Executive Education since 2016"),
            ("4", "TH", "Among 129 Universities in Sub-Saharan Africa (Times Higher Education Rankings 2024)"),
        ]):
            Stat.objects.create(value=value, suffix=suffix, label=label, order=i)

        PageSection.objects.create(
            section_type=PageSection.FEATURE, title="Explore Academics",
            body="Classrooms that thrive in vibrant discourse, based on cases that demand real world answers and applications.",
            button_text="Learn more about academics", button_url="https://ughe.org/academics/",
            image_url=f"{UP}/2026/04/DSC09176-scaled.jpg", image_position="left", background="red", order=1,
        )
        PageSection.objects.create(
            section_type=PageSection.FEATURE, title="Study at UGHE",
            body="Welcome to a next-generation university where you will have the freedom to create and then "
                 "pursue your own academic goals. At University of Global Health Equity, we empower students to "
                 "make the most of their ideas through hands-on education and intentional collaboration.",
            button_text="About admission", button_url="https://ughe.org/admission/",
            image_url=f"{UP}/2026/05/2024_ughe_onehealth_fieldschool_pmugemana1504_53707441807_o-1-scaled.jpg", image_position="right", background="light", order=2,
        )
        PageSection.objects.create(
            section_type=PageSection.NEWS, title="News & Updates",
            button_text="View all news", button_url="https://ughe.org/news-and-events/",
            background="white", order=3,
        )
        PageSection.objects.create(
            section_type=PageSection.VIDEO, title="Experience Our Impact",
            body="From classrooms to communities, UGHE is transforming healthcare across Africa and beyond. "
                 "Watch our medical students, faculty and leadership discuss the vision driving change.",
            button_text="Watch Here", button_url="https://www.youtube.com/watch?v=M2l7sCuOnHo",
            video_url="https://www.youtube.com/watch?v=M2l7sCuOnHo", background="dark", order=4,
        )

    def seed_news(self):
        news = [
            ("Walking Toward a Future Without Podoconiosis", "Centre for One Health", date(2026, 9, 30),
             "2026/08/55325793932_50dfe2e107_k-480x320.jpg"),
            ("Full recovery from trauma is not only about surviving the injury", "Alumni", date(2026, 8, 24),
             "2026/08/202605327_Kibogora_Equi-InjuryWorkshop_DNA_4-scaled-480x320.jpg"),
            ("Butaro Dialogues: UGHE and Partners Call for Innovation That Reaches Those Who Need It Most",
             "Partnerships", date(2026, 7, 27), "2026/07/IMG_2169-scaled-480x320.jpg"),
            ("UGHE hosts \"Tumenye Kaminuza\", a Campus Open Day to Strengthen Community Engagement", "News",
             date(2026, 7, 13), "2026/07/Tumenye-Kaminuza-480x320.jpg"),
            ("More Than Access: How Three Scholars Are Redefining What Global Health Looks Like", "News",
             date(2026, 6, 15), "2026/06/Collage-for-MF-480x320.png"),
            ("UGHE Ranks Fifth Globally in Medicine for Planetary Health", "News", date(2026, 5, 19),
             "2026/05/2024_ughe_onehealth_fieldschool_pmugemana1504_53707441807_o-1-scaled-480x320.jpg"),
        ]
        for title, category, day, image in news:
            NewsItem.objects.create(
                title=title, category=category, date=day,
                image_url=f"{UP}/{image}", link="https://ughe.org/news/",
            )

    def seed_footer(self):
        for i, (title, url) in enumerate([
            ("Applying", "https://ughe.org/admission/"),
            ("Student Resources", "https://ughe.org/student-resources"),
            ("Careers", "https://ughe.org/careers/"),
            ("Privacy Policy", "https://ughe.org/terms-and-privacy/"),
            ("Terms of Use", "https://www.pih.org/pages/terms"),
        ]):
            FooterLink.objects.create(title=title, url=url, order=i)

        for i, (platform, url) in enumerate([
            ("facebook", "https://www.facebook.com/ughe.org"),
            ("x", "https://twitter.com/ughe_org"),
            ("instagram", "https://www.instagram.com/ughe_org/"),
            ("linkedin", "https://www.linkedin.com/company/university-of-global-health-equity"),
        ]):
            SocialLink.objects.create(platform=platform, url=url, order=i)
