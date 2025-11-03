# Ladeinfrastruktur ETL (BNetzA)

End-to-end Mini-Data-Engineering-Projekt:
- **ETL in Python/Pandas**, 
- **PostgreSQL** + **Adminer** via Docker Compose,
- einfache **Analysen** und **Qualitätschecks**,
- **CI** via GitHub Actions.

## Architektur (Kurz)
CSV (BNetzA) → Pandas (Cleaning) → PostgreSQL (Tabelle `ladepunkte`) → SQL/Plots

## Schneller Start
```bash
# 1) Container starten (DB + Adminer)
docker compose up -d db adminer

# 2) ETL als Container (CSV → DB)
docker compose up etl

# Adminer öffnen: http://localhost:8080  (DB: ladeinfra / User: postgres / PW: postgres)