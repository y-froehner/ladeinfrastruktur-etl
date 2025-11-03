# Ladeinfrastruktur ETL (BNetzA)
[![CI](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml)

ETL-Pipeline für das BNetzA-Ladesäulenregister.  
Dieses Projekt demonstriert eine vollständige Mini-Data-Engineering-Architektur – von der CSV-Datei bis zur PostgreSQL-Datenbank mit Docker, Adminer und einer automatisierten CI-Pipeline über GitHub Actions.

---

## Inhaltsverzeichnis
1. [Features](#features)
2. [Architekturüberblick](#architekturüberblick)
3. [Datenbereinigung & Insights](#datenbereinigung--insights)
4. [Visualisierungen](#visualisierungen)
5. [Schnellstart](#schnellstart)
6. [Projektstruktur](#projektstruktur)
7. [Nützliche SQL-Queries](#nützliche-sql-queries)
8. [CI-Pipeline](#ci-pipeline)
9. [Autor](#autor)

---

## Features
- ETL mit Python und Pandas zur Bereinigung, Transformation und Standardisierung von Rohdaten  
- PostgreSQL + Adminer als Datenbank- und UI-Schicht über Docker Compose  
- Automatische Qualitätschecks für fehlende Werte, Typvalidierung und Ausreißer-Erkennung  
- CI-Integration über GitHub Actions (Tests + Smoke-Test bei jedem Push)  
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
↑  
Git Push → GitHub Actions (CI: Tests & Smoke)

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

## Visualisierungen

Einige Beispiel-Grafiken aus der explorativen Analyse:

### 1. Top 10 Bundesländer – Anzahl öffentlicher Ladeeinrichtungen
![Top 10 Bundesländer](output/ladepunkte_pro_bundesland_top10.png)

### 2. Inbetriebnahmen pro Jahr
![Inbetriebnahmen pro Jahr](output/inbetriebnahmen_pro_jahr.png)

### 3. Geografische Verteilung (Stichprobe n=5000)
![Verteilung Deutschland](output/ladepunkte_scatter_map_sample.png)

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

## CI-Pipeline

Jeder Push triggert automatisch eine Pipeline unter `.github/workflows/ci.yml`, die prüft:
- ob der Code fehlerfrei importierbar ist
- ob alle Dependencies installiert werden können
- ob das ETL-Skript erfolgreich ausgeführt werden kann

---

## Autor

**Yannis Fröhner**  
Data Engineering & Analytics  
GitHub: [y-froehner](https://github.com/y-froehner)
