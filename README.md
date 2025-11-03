# Ladeinfrastruktur ETL (BNetzA)
[![CI](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml)
[![Publish](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/publish.yml/badge.svg)](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/publish.yml)

ETL-Pipeline für das BNetzA-Ladesäulenregister.  
Dieses Projekt demonstriert eine vollständige Mini-Data-Engineering-Architektur – von der CSV-Datei bis zur PostgreSQL-Datenbank mit Docker, Adminer und einer automatisierten CI/CD-Pipeline über GitHub Actions.

---

## Features
- ETL mit Python und Pandas zur Bereinigung, Transformation und Standardisierung von Rohdaten  
- PostgreSQL + Adminer als Datenbank- und UI-Schicht über Docker Compose  
- Automatische Qualitätschecks für fehlende Werte, Typvalidierung und Ausreißer-Erkennung  
- CI/CD-Integration über GitHub Actions (Tests + automatischer Docker-Build & Push nach GHCR)  
- Reproduzierbare Umgebung durch Containerisierung mit Docker

---

## Architekturüberblick

CSV (BNetzA)  
↓  
Pandas (Cleaning & Transformation)  
↓  
PostgreSQL (Tabelle ladepunkte)  
↓  
SQL-Queries und Analysen  
↓  
Deployment des ETL-Containers über GitHub Actions → GHCR

---

## Datenbereinigung & Insights

Die Bereinigungsschritte im ETL-Skript umfassen:
- Vereinheitlichung von Spaltennamen (z. B. `Bundesland`, `Betreiber`, `Steckertyp`)
- Entfernung von Duplikaten (mehrfache Ladesäulen-Einträge)
- Typkonvertierung (Datum, numerische Werte, Koordinaten)
- Entfernung leerer oder fehlerhafter Zeilen
- Ersetzung inkonsistenter Werte (z. B. `None`, `n/a`, `-`)
- Berechnung neuer Felder (z. B. Installationsjahr, Leistungskategorie)

Beispiele aus der explorativen Analyse (Pandas/SQL):
- Rund **100.000 Ladepunkte** bundesweit in der letzten CSV-Version
- **NRW, Bayern, Baden-Württemberg** = ~50 % aller Ladesäulen
- Deutliches Wachstum seit 2020, vor allem bei **Schnellladern (DC)**
- Typische Qualitätsprobleme: unvollständige Adressfelder, fehlende Postleitzahlen

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
.github/     - CI- und CD-Workflows (GitHub Actions)
```

---

## Nützliche SQL-Queries

```sql
SELECT COUNT(*) AS zeilen FROM ladepunkte;

CREATE INDEX IF NOT EXISTS idx_ladepunkte_bundesland
ON ladepunkte ("Bundesland");
```

**Häufige Fehler:**  
Wenn du die Tabelle neu laden willst, aber Materialized Views existieren, kann es nötig sein, vorher `DROP MATERIALIZED VIEW ... CASCADE;` auszuführen.

---

## CI/CD

### Continuous Integration (CI)
Jeder Push triggert automatisch eine Pipeline unter `.github/workflows/ci.yml`, die prüft:
- ob der Code fehlerfrei importierbar ist
- ob alle Dependencies installiert werden können
- ob das ETL-Skript erfolgreich ausgeführt werden kann

### Continuous Delivery (CD)
Der Workflow `.github/workflows/publish.yml` erstellt automatisch ein Docker-Image des ETL-Prozesses und pusht es in den GitHub Container Registry (GHCR).  
Dadurch kann das Projekt auf jedem Rechner mit `docker pull ghcr.io/y-froehner/ladeinfrastruktur-etl:latest` gestartet werden.

---

## Autor

**Yannis Fröhner**  
Data Engineering & Analytics  
GitHub: [y-froehner](https://github.com/y-froehner)

