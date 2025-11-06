# Use an official lightweight Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies for psycopg2, requests, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run the Django app with Gunicorn (production-ready)
CMD ["gunicorn", "luas_forecast.wsgi:application", "--bind", "0.0.0.0:8000"]
