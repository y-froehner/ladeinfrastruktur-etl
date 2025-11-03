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

## Datenbereinigung & Qualitätschecks

Im ETL-Prozess wurden die Rohdaten des BNetzA-Ladesäulenregisters umfassend bereinigt und harmonisiert:

- **Spaltennamen vereinheitlicht** (`CamelCase` → `snake_case`)  
- **Numerische Felder** von Komma- in Punktnotation konvertiert (`"2,5"` → `2.5`)  
- **Fehlende Werte** in optionalen Feldern wie Betreiber, Ort oder Standort ersetzt oder ausgeschlossen  
- **Ungültige Koordinaten** und Postleitzahlen verworfen  
- **Doppelte Einträge** anhand eindeutiger Kombination aus Betreiber + Adresse entfernt  
- **Datumsfelder** (z. B. Inbetriebnahme) auf ISO-Format normalisiert (`YYYY-MM-DD`)  
- **Datentypen geprüft und konsistent gecastet** (z. B. Ladeleistung → float, PLZ → int)  

Ziel war es, ein **analytisch sauberes und typstabiles Dataset** in PostgreSQL zu erhalten.

---

## Erste Insights aus der Pandas-Analyse

Nach der Bereinigung wurden grundlegende Kennzahlen und Muster analysiert:

| Kennzahl | Wert / Beobachtung |
|-----------|--------------------|
| **Gesamtzahl Ladepunkte** | ca. 97 000 |
| **Top 3 Bundesländer** | Bayern, NRW, Baden-Württemberg |
| **Durchschnittliche Ladeleistung** | ca. 44 kW |
| **Anteil Schnelllader (>50 kW)** | ~18 % |
| **Zuwachsrate 2024 vs 2023** | +22 % neue Ladepunkte |
| **Anteil AC vs DC-Ladung** | 81 % AC / 19 % DC |

Diese Kennzahlen stammen aus einer explorativen Analyse in `explore_data.py`  
und dienen zur Plausibilisierung der Datenqualität und des regionalen Ausbaustands.

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
- ~97 000 Datensätze, 47 Spalten (BNetzA-Register)  
- Typbereinigung (Komma/Punkt, Datumsformat, Duplikate)  
- Docker-basierte Reproduzierbarkeit  
- SQL-Auswertung über Adminer möglich  

---

## Autor
**Yannis Fröhner**  
Data Engineering & Analytics  
[GitHub: y-froehner](https://github.com/y-froehner)

