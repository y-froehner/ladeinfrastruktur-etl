# Ladeinfrastruktur ETL (BNetzA)
[![CI](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml)

ETL-Pipeline für das BNetzA-Ladesäulenregister.  
Dieses Projekt demonstriert eine vollständige Mini-Data-Engineering-Architektur – von der CSV-Datei bis zur PostgreSQL-Datenbank mit Docker, Adminer und einer automatisierten CI-Pipeline über GitHub Actions.

---

## Features
- ETL mit Python und Pandas zur Bereinigung, Transformation und Standardisierung von Rohdaten  
- PostgreSQL + Adminer als Datenbank- und UI-Schicht über Docker Compose  
- Qualitätschecks für Typprüfung, fehlende Werte und Datumsfelder  
- CI/CD-Integration über GitHub Actions (Linting und Smoke-Test bei jedem Push)  
- Reproduzierbare Umgebung durch Containerisierung mit Docker

---

## Architekturüberblick
```
CSV (BNetzA)
   ↓
Pandas (Cleaning & Transformation)
   ↓
PostgreSQL (Tabelle `ladepunkte`)
   ↓
SQL-Queries und Analysen
```

---

## Schnellstart
```bash
# Container starten (PostgreSQL + Adminer)
docker compose up -d db adminer

# ETL ausführen (CSV → Datenbank)
docker compose up etl

# Adminer öffnen:
# http://localhost:8080
# (DB: ladeinfra | User: postgres | PW: postgres)
```

---

## Projektstruktur
```
etl/         - ETL-Skripte (etl.py, load_to_db.py, config.py)
data/        - CSV-Dateien (raw + cleaned)
sql/         - Beispiel-Queries und Materialized Views
output/      - Diagramme oder Analyseergebnisse
.github/     - CI-Workflow (GitHub Actions)
docker-compose.yml - Services: db, adminer, etl
Dockerfile   - Image für ETL-Container
requirements.txt - Python-Abhängigkeiten
```

---

## Nützliche SQL-Queries
```sql
-- Anzahl Zeilen prüfen
SELECT COUNT(*) AS zeilen FROM ladepunkte;

-- Index für häufige Filter
CREATE INDEX IF NOT EXISTS idx_ladepunkte_bundesland
ON ladepunkte ("Bundesland");
```

---

## CI/CD
Jeder Push triggert automatisch eine Pipeline unter  
`.github/workflows/ci.yml`, die prüft, ob:
- sich der Code fehlerfrei importieren lässt  
- die Abhängigkeiten korrekt installiert werden  
- das ETL-Skript erfolgreich ausgeführt werden kann (Smoke-Test)

Den aktuellen Status siehst du über das Badge oben oder im Actions-Tab des Repos.

---

## Voraussetzungen
- Docker Desktop installiert und laufend  
- Git und GitHub Repository  
- Optional: Python 3.11 lokal für Entwicklungs-Runs

---

## Autor
**Yannis Fröhner**  
Data Engineering & Analytics  
[GitHub: y-froehner](https://github.com/y-froehner)