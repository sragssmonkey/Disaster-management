# Set working directory
WORKDIR /app

# Set Django env variables
ENV DJANGO_SETTINGS_MODULE=Disaster.settings
ENV DJANGO_SECRET_KEY=your-secret-key
ENV DEBUG=False
ENV ALLOWED_HOSTS=.onrender.com
ENV STATIC_ROOT=/app/staticfiles

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project code
COPY . .

# Collect static & run
CMD python manage.py collectstatic --noinput && \
    gunicorn Disaster.wsgi:application --bind 0.0.0.0:8000
