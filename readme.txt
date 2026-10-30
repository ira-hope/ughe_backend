
                    UGHE TEST WEB APP
   Next.js (frontend) + Django REST API (backend) + PostgreSQL


Author: IRADUKUNDA Hope


----------------------------------------------------------
1. GITHUB REPOSITORIES (public)
----------------------------------------------------------
Backend (Django)  : https://github.com/ira-hope/ughe_backend.git
Frontend (Next.js): https://github.com/ira-hope/ughe_frontend.git


----------------------------------------------------------
2. LOGIN CREDENTIALS (predefined)
----------------------------------------------------------
Frontend login (http://localhost:3000/login)
    Username: ughe
    Password: Ughe@2026

Django Admin (http://localhost:8000/admin) - to add/edit content
    Username: admin
    Password: Admin@2026

These accounts are created automatically when the backend starts
(command: python manage.py create_default_users). They can be changed
in the backend .env file.


----------------------------------------------------------
3. WHAT YOU NEED INSTALLED
----------------------------------------------------------
- Docker Desktop (make sure it is running)
- Git
(Optional, only to run without Docker: Python 3.12+, Node.js 20+, PostgreSQL 16)


----------------------------------------------------------
4. HOW TO RUN WITH DOCKER (recommended)
----------------------------------------------------------
Step 1 - Clone both repositories into the same folder:
    git clone https://github.com/ira-hope/ughe_backend.git ughe-backend
    git clone https://github.com/ira-hope/ughe_frontend.git ughe-frontend

Step 2 - Start the backend (Django + PostgreSQL):
    cd ughe-backend
    copy .env.example .env          (Windows)
    cp .env.example .env            (Mac/Linux)
    docker-compose up --build

    When it starts it automatically:
      a) creates the database tables (migrate)
      b) creates the predefined users (create_default_users)
      c) loads sample UGHE content into the database (seed_content)
      d) runs the API on http://localhost:8000

Step 3 - Start the frontend (Next.js), in a NEW terminal:
    cd ughe-frontend
    docker-compose up --build

Step 4 - Open the app:
    http://localhost:3000        -> you are sent to the login page
    Log in with ughe / Ughe@2026 -> the home page loads the content from Django

Step 5 - Change the content:
    Open http://localhost:8000/admin, log in with admin / Admin@2026,
    edit or add any item, then refresh http://localhost:3000.

To stop: press Ctrl+C, then run "docker-compose down" in each folder.
To reset everything (delete the database): "docker-compose down -v" in ughe-backend.
(Newer Docker versions also accept "docker compose" with a space.)

Note: Docker runs its OWN PostgreSQL (the "db" container). It does not use any
PostgreSQL installed on your PC. Its database name, user and password are read
from the .env file (POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD), and Django
uses the same values, so they always match. If you change them after the first
run, run "docker-compose down -v" so the database is created again.


----------------------------------------------------------
5. HOW TO RUN WITHOUT DOCKER (optional)
----------------------------------------------------------
Backend:
    cd ughe-backend
    python -m venv venv
    venv\Scripts\activate             (Windows)   |  source venv/bin/activate (Mac/Linux)
    pip install -r requirements.txt
    Create the database in your local PostgreSQL (psql):  create database ughe_db;
    Default connection in config/settings.py: database "ughe_db", user "postgres",
    no password, localhost:5432 (no .env is needed for this local run).
    If your local PostgreSQL user has a password, set it first:
        set POSTGRES_PASSWORD=yourpassword        (Windows cmd)
        export POSTGRES_PASSWORD=yourpassword     (Mac/Linux)
    python manage.py migrate
    python manage.py create_default_users
    python manage.py seed_content
    python manage.py runserver

Frontend:
    cd ughe-frontend
    copy .env.example .env.local
    npm install
    npm run dev                       -> http://localhost:3000


----------------------------------------------------------
6. WHAT CAN BE MANAGED IN DJANGO ADMIN (nothing is hardcoded)
----------------------------------------------------------
Every item shown on the home page is stored in PostgreSQL and comes from
the API. The frontend only contains the layout and colours.

- Site settings     : site name, header logo, footer logo, tagline, campus
                      address, office hours, phone, email, Kigali office, copyright
- Navigation items  : main menu, dropdown children (pick a "parent"),
                      and the top bar buttons (Apply, Get Involved, ...)
- Slides            : hero slideshow. Each slide is an IMAGE or a VIDEO
                      (upload a file, or paste a link: image URL, MP4 URL or
                      YouTube URL). One slide = no arrows; many slides =
                      auto-play with arrows and dots.
- Home page sections: the blocks under the slideshow and their ORDER.
                      Types: Facts & stats, Text + image, News list, Video.
                      Each has title, text, button, image, background colour
                      and image position (left/right).
- Stats             : the numbers in "Facts & Stats"
- News items        : cards in "News & Updates" (newest 6 are shown)
- Footer links      : links in the footer bottom bar
- Social links      : Facebook, X, Instagram, LinkedIn, YouTube icons

Images and videos can be uploaded or linked. Uploaded files are saved
in the backend "media" folder (a Docker volume).
The sample content (texts, images, YouTube video) was taken from
https://ughe.org and is loaded by the command "python manage.py seed_content"
(use "--force" to reload it).


----------------------------------------------------------
7. REST API ENDPOINTS (Django REST Framework)
----------------------------------------------------------
POST /api/login/    {username, password} -> {token, username}
POST /api/logout/   deletes the token                 (token required)
GET  /api/site/     site name + logo for the login page (public)
GET  /api/home/     all home page content              (token required)

The frontend sends the token in the header:  Authorization: Token <token>
Without a valid token /api/home/ returns 401 and the user is sent to login.


----------------------------------------------------------
8. FONT
----------------------------------------------------------
Museo Slab (used on ughe.org) is a paid font (Adobe Fonts / MyFonts), so I used
"Roboto Slab", one of the allowed alternatives. I found it on Google Fonts:
https://fonts.google.com/specimen/Roboto+Slab
It is included in ughe-frontend/app/layout.js with Next.js "next/font/google"
and applied to the whole page in app/globals.css (font-family: var(--font-slab)).
Rockwell and Courier New are set as fallback fonts.


----------------------------------------------------------
9. COLOURS (taken from the ughe.org stylesheet)
----------------------------------------------------------
UGHE red    #ae152d   buttons, titles, numbers
UGHE maroon #9d2235   footer bottom bar, login background
UGHE gold   #eba720   slideshow button, highlights
Dark        #252525   text, footer
Grey        #696969   secondary text
Light grey  #f5f5f5   light section background
They are defined once at the top of ughe-frontend/app/globals.css.


----------------------------------------------------------
10. PROJECT STRUCTURE
----------------------------------------------------------
ughe-backend/
  config/settings.py        settings (PostgreSQL, REST framework, CORS)
  config/urls.py            /admin and /api routes
  content/models.py         database tables for all content
  content/admin.py          Django Admin screens
  content/serializers.py    turns database rows into JSON
  content/views.py          login, logout and home API
  content/management/commands/
      create_default_users.py   creates the predefined users
      seed_content.py           loads sample UGHE content
  requirements.txt          Python libraries used
  Dockerfile, docker-compose.yml, .env.example

ughe-frontend/
  app/layout.js             page layout + font loading
  app/globals.css           colours and styles
  app/login/page.js         login page
  app/page.js               home page (protected)
  components/               Header, Slideshow, StatsSection, FeatureSection,
                            NewsSection, VideoSection, Footer
  lib/api.js                calls to the Django API
  lib/media.js              YouTube and date helpers
  package.json              Node libraries used
  Dockerfile, docker-compose.yml, .env.example


----------------------------------------------------------
11. LIBRARIES USED
----------------------------------------------------------
Backend (requirements.txt): Django 5.1, djangorestframework 3.15 (REST API +
token login), django-cors-headers (allows the frontend to call the API),
psycopg2-binary (PostgreSQL driver), Pillow (image uploads).
Frontend (package.json): Next.js 14 (App Router), React 18.
Docker images: python:3.12-slim, node:20-alpine, postgres:16-alpine.


----------------------------------------------------------
12. APPROACH / STEPS I FOLLOWED
----------------------------------------------------------
1. Studied https://ughe.org to list the home page parts (header with menu and
   buttons, hero slideshow, Facts & Stats, Explore Academics, Study at UGHE,
   News & Updates, Experience Our Impact video, footer) and read its colours
   and font from the website stylesheet.
2. Created the Django project "config" and the app "content", then designed one
   model per kind of content so every item can be added in Django Admin.
3. Connected Django to PostgreSQL using environment variables.
4. Built the REST API with Django REST Framework and token authentication.
   The login endpoint checks the predefined credentials and returns a token.
5. Wrote two management commands: one creates the predefined users, the other
   loads sample content from ughe.org into the database.
6. Created the Next.js app: a login page, and a protected home page that gets
   all content from /api/home/ and renders each section in the order set in admin.
7. Built a slideshow that supports one or many slides, images or videos
   (MP4 or YouTube).
8. Styled the pages with the UGHE colours and Roboto Slab, and made the layout
   responsive (desktop, tablet, phone).
9. Added a Dockerfile and docker-compose.yml to each repository and tested the
   full flow: login -> home page -> edit content in admin -> refresh frontend.

Resources used: Django docs (docs.djangoproject.com), Django REST Framework docs
(django-rest-framework.org), Next.js docs (nextjs.org/docs), Docker docs
(docs.docker.com), Google Fonts, and the UGHE website for content and images.
