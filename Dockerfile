

# ---- Base image ----
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install dependencies system-wide (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=luas_forecast.settings

# Collect static files (optional if not using storage service)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start the app with Gunicorn
CMD ["gunicorn", "luas_forecast.wsgi:application", "--bind", "0.0.0.0:8000"]
