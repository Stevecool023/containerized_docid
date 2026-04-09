FROM python:3.11-slim


# Prevent Python from writing pyc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app


RUN mkdir -p /app/logs


# Install system deps if needed (e.g. for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
   libpq5 \
   && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy application code
COPY . .


# Expose Flask port
EXPOSE 5001


# Run gunicorn (production)
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]