# Use Python 3.11 (needed for contourpy 1.3.3)
FROM python:3.11-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project code
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=Disaster.settings
ENV DJANGO_SECRET_KEY=your-secret-key
ENV DEBUG=False
ENV ALLOWED_HOSTS=.onrender.com

# Collect static files at runtime
CMD python manage.py collectstatic --noinput && \
    gunicorn Disaster.wsgi:application --bind 0.0.0.0:8000
