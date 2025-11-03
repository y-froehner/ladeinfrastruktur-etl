# Ladeinfrastruktur ETL (BNetzA)
[![CI](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/y-froehner/ladeinfrastruktur-etl/actions/workflows/ci.yml)

ETL-Pipeline für das BNetzA-Ladesäulenregister.  
Dieses Projekt zeigt eine vollständige Mini-Data-Engineering-Architektur:  
Vom CSV-Rohdatensatz bis zur PostgreSQL-Datenbank – automatisiert, containerisiert und CI-getestet.

---

## Features
- ETL-Prozess in **Python + Pandas** zur Bereinigung, Typprüfung und Transformation  
- **PostgreSQL** als relationale Zieldatenbank  
- **Adminer** als webbasierte UI zur Dateninspektion  
- **Docker Compose** orchestriert alle Services (ETL, Datenbank, Adminer)  
- **CI-Pipeline über GitHub Actions** prüft Codequalität und ETL-Funktionalität  
- Reproduzierbare und isolierte Umgebung – kein Setup-Chaos auf dem lokalen System  

---

## Architekturüberblick
```
CSV (BNetzA)
   ↓
Python + Pandas (ETL-Transformation in Container)
   ↓
PostgreSQL (Tabelle `ladepunkte`, bereitgestellt im DB-Container)
   ↓
SQL-Abfragen und Analysen (via Adminer-Webinterface)
   ↓
Docker Compose (orchestriert ETL-, DB- und Adminer-Container)
```

**Erläuterung:**  
Alle Komponenten laufen als Docker-Container:
- `etl` verarbeitet CSV-Dateien und lädt sie in die Datenbank.  
- `db` stellt PostgreSQL bereit.  
- `adminer` bietet eine Weboberfläche zur Inspektion und Analyse der Daten.  

So bleibt die gesamte Pipeline **plattformunabhängig**, **reproduzierbar** und **leicht teilbar**.

---

## Schnellstart
```bash
# 1) Datenbank + Adminer starten
docker compose up -d db adminer

# 2) ETL-Job ausführen (lädt CSV in PostgreSQL)
docker compose up etl

# 3) Adminer im Browser öffnen:
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
docker-compose.yml - Definition der Services (db, adminer, etl)
Dockerfile   - Image für ETL-Container
requirements.txt - Python-Abhängigkeiten
```

---

## Nützliche SQL-Queries
```sql
-- Anzahl Zeilen prüfen
SELECT COUNT(*) AS zeilen FROM ladepunkte;

-- Index für häufige Filter (beschleunigt Abfragen nach Bundesland)
CREATE INDEX IF NOT EXISTS idx_ladepunkte_bundesland
ON ladepunkte ("Bundesland");
```

---

## CI/CD
Jeder Push triggert automatisch eine Pipeline unter  
`.github/workflows/ci.yml`, die prüft, ob:
- sich der Code fehlerfrei importieren lässt  
- alle Abhängigkeiten installiert werden können  
- der ETL-Container erfolgreich gebaut und ausgeführt werden kann  

Das Ergebnis siehst du über das Badge oben oder im „Actions“-Tab des Repos.  

---

## Voraussetzungen
- **Docker Desktop** installiert und laufend  
- **Git** zur Versionskontrolle  
- Optional: **Python 3.11** für lokale Entwicklung und Tests  

---

## Highlights
- ~97k Datensätze, 47 Spalten (BNetzA-Register)  
- Typbereinigung (Komma/Punkt, Datumsformat, Duplikate)  
- Docker-basierte Reproduzierbarkeit  
- SQL-Auswertung über Adminer möglich  

---

## Autor
**Yannis Fröhner**  
Data Engineering & Analytics  
[GitHub: y-froehner](https://github.com/y-froehner)

---

⭐ Wenn dir dieses Projekt gefällt oder du etwas Ähnliches bauen willst, kannst du es gerne starren oder forken.
