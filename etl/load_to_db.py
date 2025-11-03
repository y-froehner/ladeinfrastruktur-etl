# etl/load_to_db.py
import pandas as pd
from sqlalchemy import create_engine, text
from etl.config import PROCESSED_CSV, SQLALCHEMY_URL

def load_dataframe_to_postgres():
    print("🚀 load_to_db", flush=True)
    print("📄 Lese CSV:", PROCESSED_CSV, flush=True)

    df = pd.read_csv(PROCESSED_CSV, low_memory=False)

    # ——— Typen harmonisieren (Komma -> Punkt, Datum parsen) ———
    def to_float(series):
        return (series.astype(str)
                      .str.replace(",", ".", regex=False)
                      .str.replace(r"[^0-9\.\-]", "", regex=True)
                      .replace({"": None})
                      .astype(float))

    numeric_cols = ["Anzahl Ladepunkte", "Nennleistung Ladeeinrichtung [kW]"]
    coord_cols   = ["Breitengrad", "Längengrad"]
    date_col     = "Inbetriebnahmedatum"

    for c in numeric_cols:
        if c in df.columns:
            df[c] = to_float(df[c])
    for c in coord_cols:
        if c in df.columns:
            df[c] = to_float(df[c])
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")

    engine = create_engine(SQLALCHEMY_URL, pool_pre_ping=True)
    base_table = "ladepunkte"

    print("🔧 Schreibe Staging-Tabelle …", flush=True)
    df.to_sql("_ladepunkte_staging", engine, if_exists="replace", index=False, method="multi", chunksize=5000)

    with engine.begin() as conn:
        print("🔁 Swappe Staging → produktiv …", flush=True)
        # produktiv ersetzen
        conn.execute(text(f'DROP TABLE IF EXISTS {base_table} CASCADE'))
        conn.execute(text(f'ALTER TABLE "_ladepunkte_staging" RENAME TO {base_table}'))

        # Indizes
        conn.execute(text(f'CREATE INDEX IF NOT EXISTS idx_{base_table}_bundesland ON {base_table} ("Bundesland")'))
        conn.execute(text(f'CREATE INDEX IF NOT EXISTS idx_{base_table}_plz        ON {base_table} ("Postleitzahl")'))
        conn.execute(text(f'CREATE INDEX IF NOT EXISTS idx_{base_table}_status     ON {base_table} ("Status")'))
        if "Breitengrad" in df.columns:
            conn.execute(text(f'CREATE INDEX IF NOT EXISTS idx_{base_table}_breite ON {base_table} ("Breitengrad")'))
        if "Längengrad" in df.columns:
            conn.execute(text(f'CREATE INDEX IF NOT EXISTS idx_{base_table}_laenge ON {base_table} ("Längengrad")'))

        # Materialized View neu aufbauen (immer gültiges Schema)
        print("🏗️  Rebuild Materialized View …", flush=True)
        conn.execute(text('DROP MATERIALIZED VIEW IF EXISTS mv_neu_pro_monat_bundesland'))
        conn.execute(text("""
            CREATE MATERIALIZED VIEW mv_neu_pro_monat_bundesland AS
            SELECT
                date_trunc('month', "Inbetriebnahmedatum")::date AS monat,
                "Bundesland",
                COUNT(*) AS anzahl
            FROM ladepunkte
            WHERE "Inbetriebnahmedatum" IS NOT NULL
            GROUP BY 1, 2
        """))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_mv_monat ON mv_neu_pro_monat_bundesland (monat)'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS idx_mv_bundesland ON mv_neu_pro_monat_bundesland ("Bundesland")'))

    print(f"✅ {len(df):,} Zeilen geladen & Views aktualisiert.", flush=True)

if __name__ == "__main__":
    load_dataframe_to_postgres()