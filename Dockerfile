# Python image used to run the Django backend
FROM python:3.12-slim

# Do not create .pyc files and show logs immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install the Python libraries first (cached between builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

EXPOSE 8000

# On start: create tables, create predefined users, load sample content, run the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py create_default_users && python manage.py seed_content && python manage.py runserver 0.0.0.0:8000"]
