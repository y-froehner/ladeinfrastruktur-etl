# Dockerfile
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Systemabhängigkeiten (klein halten)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
 && rm -rf /var/lib/apt/lists/*

# Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Nur Code & Config — keine CSVs
COPY etl/ etl/
COPY requirements.txt .
COPY explore_data.py .

# Standard: unbuffered logs
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "-m", "etl.etl"]