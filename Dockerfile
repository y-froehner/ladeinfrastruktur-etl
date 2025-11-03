# Dockerfile
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# 🧱 Systemabhängigkeiten (klein halten)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
 && rm -rf /var/lib/apt/lists/*

# 🐍 Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Nur was zum Lauf gebraucht wird
COPY etl/ etl/
COPY requirements.txt .
COPY explore_data.py .
COPY data/processed_ladesaeulen.csv data/
COPY data/Ladesaeulenregister_BNetzA_2025-10-23.csv data/

# 🔧 Standard-Einstellung: ungebufferte Logs
ENV PYTHONUNBUFFERED=1

# 🚀 Standardkommando (führt dein ETL-Skript aus)
CMD ["python", "-m", "etl.etl"]