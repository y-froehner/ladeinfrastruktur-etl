# Ladeinfrastruktur ETL (BNetzA)
[![CI](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml)

ETL-Pipeline für das BNetzA-Ladesäulenregister.  
Dieses Projekt demonstriert eine vollständige Mini-Data-Engineering-Architektur – von der CSV-Datei bis zur PostgreSQL-Datenbank mit Docker, Adminer und einer automatisierten CI-Pipeline über GitHub Actions.

---

## Inhaltsverzeichnis
1. [Features](#features)  
2. [Architekturüberblick](#architekturüberblick)  
3. [Datenbereinigung & Insights](#datenbereinigung--insights)  
4. [Schnellstart](#schnellstart)  
5. [Projektstruktur](#projektstruktur)  
6. [Nützliche-SQL-Queries](#nützliche-sql-queries)  
7. [CI-Pipeline](#ci-pipeline)  
8. [Autor](#autor)

---

## Features
- ETL mit Python und Pandas zur Bereinigung, Transformation und Standardisierung von Rohdaten  
- PostgreSQL + Adminer als Datenbank- und UI-Schicht über Docker Compose  
- Automatische Qualitätschecks für fehlende Werte, Typvalidierung und Ausreißer-Erkennung  
- CI-Integration über GitHub Actions (Smoke Tests und Linting)  
- Reproduzierbare Umgebung durch Containerisierung mit Docker

---

## Architekturüberblick

**ETL- & Datenfluss**

CSV (BNetzA)  
↓  
Pandas (Cleaning & Transformation)  
↓  
PostgreSQL (Tabelle `ladepunkte`)  
↓  
SQL-Queries und Analysen  
↑  
Git push (Branch `main`)  
↓  
GitHub Actions (CI: Linting, Smoke Tests, ETL-Check)

**Beschreibung:**  
Diese Darstellung kombiniert den fachlichen Datenfluss und den technischen Entwicklungszyklus.  
Jeder Push in den `main`-Branch löst automatisch eine CI-Pipeline aus, die sicherstellt, dass der Code lauffähig ist und der ETL-Prozess erfolgreich durchläuft.

---

## Datenbereinigung & Insights

**Bereinigungsschritte im ETL-Skript:**
- Vereinheitlichung von Spaltennamen (`Bundesland`, `Betreiber`, `Steckertyp`)  
- Entfernung von Duplikaten und fehlerhaften Zeilen  
- Typkonvertierung (Datum, numerische Werte, Koordinaten)  
- Ersetzung inkonsistenter Werte (`None`, `n/a`, `-`)  
- Berechnung neuer Felder (z. B. Installationsjahr, Leistungskategorie)

**Beobachtungen aus der Analyse:**
- Rund **100.000 Ladepunkte** in der aktuellen CSV-Version  
- **NRW, Bayern und Baden-Württemberg** stellen etwa 50 % aller Ladesäulen  
- Starkes Wachstum seit 2020, besonders bei **Schnellladern (DC)**  
- Häufige Datenprobleme: unvollständige Adressen und fehlende Postleitzahlen  

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
.github/     - CI-Workflows (GitHub Actions)
```

---

## Nützliche SQL-Queries

```sql
SELECT COUNT(*) AS zeilen FROM ladepunkte;

CREATE INDEX IF NOT EXISTS idx_ladepunkte_bundesland
ON ladepunkte ("Bundesland");
```

**Häufiger Fehler:**  
Falls Materialized Views existieren, müssen sie vor einem erneuten Laden der Tabelle entfernt werden:  
```sql
DROP MATERIALIZED VIEW IF EXISTS mv_neu_pro_monat_bundesland CASCADE;
```

---

## CI-Pipeline

Jeder Push oder Pull Request auf `main` triggert automatisch den Workflow  
`.github/workflows/ci.yml`, der folgende Schritte durchführt:

1. Repository auschecken  
2. Python-Umgebung (3.11) einrichten  
3. Dependencies installieren  
4. Smoke-Test des ETL-Skripts ausführen  

Dieser Prozess stellt sicher, dass das Projekt stabil, reproduzierbar und jederzeit lauffähig bleibt.

---

## Autor

**Yannis Fröhner**  
Data Engineering & Analytics  
GitHub: [y-froehner](https://github.com/y-froehner)
