import os
import pandas as pd
from etl.config import CSV_PATH

def load_raw_csv(path: str) -> pd.DataFrame:
    """
    CSV laden und die echte Header-Zeile 'promoten'.
    (In deinem Datensatz steht der Kopf in Zeile 10 = header=9.)
    """
    df = pd.read_csv(
        path,
        sep=";",
        encoding="latin1",
        low_memory=False,
        header=9,
        skip_blank_lines=True
    )

    # erste gelesene Zeile enthält die echten Spaltennamen
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    # 'Unnamed: ...' Spalten entfernen, Spaltennamen trimmen
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
    df.columns = df.columns.astype(str).str.strip()
    return df


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Leichte Bereinigung:
    - numerische Felder mit Komma in Floats umwandeln (z. B. kW, Koordinaten)
    - Datum parsen
    """
    # Leistungsspalten (kW)
    for col in df.columns:
        if "kW" in str(col) or "Leistung" in str(col):
            df[col] = (
                df[col].astype(str)
                      .str.replace(",", ".", regex=False)
                      .str.extract(r"([\-]?\d+(?:\.\d+)?)")[0]
                      .astype(float)
            )

    # Datum
    if "Inbetriebnahmedatum" in df.columns:
        df["Inbetriebnahmedatum"] = pd.to_datetime(
            df["Inbetriebnahmedatum"], dayfirst=True, errors="coerce"
        )

    # Koordinaten
    if {"Breitengrad", "Längengrad"}.issubset(df.columns):
        for c in ["Breitengrad", "Längengrad"]:
            df[c] = (
                df[c].astype(str)
                    .str.replace(",", ".", regex=False)
                    .str.extract(r"([\-]?\d+(?:\.\d+)?)")[0]
                    .astype(float)
            )
    return df


def quality_checks(df: pd.DataFrame) -> dict:
    """
    Kleine Qualitäts-Kennzahlen, damit du im Gespräch was zeigen kannst.
    """
    return {
        "rows": len(df),
        "cols": df.shape[1],
        "null_rate_bundesland":
            df["Bundesland"].isna().mean() if "Bundesland" in df.columns else None,
        "null_rate_koordinaten":
            float(df[["Breitengrad","Längengrad"]].isna().any(axis=1).mean())
            if {"Breitengrad","Längengrad"}.issubset(df.columns) else None,
        "min_date":
            str(df["Inbetriebnahmedatum"].min()) if "Inbetriebnahmedatum" in df.columns else None,
        "max_date":
            str(df["Inbetriebnahmedatum"].max()) if "Inbetriebnahmedatum" in df.columns else None,
    }


def save_artifacts(df: pd.DataFrame):
    """
    Speichert ein aufgeräumtes CSV und eine einfache Grafik.
    """
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/processed_ladesaeulen.csv", index=False)
    print("💾 Saved: data/processed_ladesaeulen.csv")

    if "Bundesland" in df.columns:
        import matplotlib.pyplot as plt
        os.makedirs("output", exist_ok=True)
        top_states = df["Bundesland"].value_counts().head(10)
        plt.figure(figsize=(10, 6))
        top_states.plot(kind="bar")
        plt.title("Top 10 Bundesländer – Anzahl öffentlicher Ladeeinrichtungen")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig("output/ladepunkte_pro_bundesland_top10.png", dpi=150)
        print("📈 Saved: output/ladepunkte_pro_bundesland_top10.png")


def main():
    print("▶️ Lade CSV:", CSV_PATH)
    df = load_raw_csv(CSV_PATH)
    print("Shape raw:", df.shape)

    df = basic_clean(df)
    print("Shape clean:", df.shape)

    checks = quality_checks(df)
    print("Quality:", checks)

    save_artifacts(df)


if __name__ == "__main__":
    main()