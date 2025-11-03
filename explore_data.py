import pandas as pd
import sys
sys.stdout.reconfigure(line_buffering=True)

# CSV aus dem Unterordner "data" einlesen
df = pd.read_csv(
    "data/Ladesaeulenregister_BNetzA_2025-10-23.csv",
    sep=";",
    encoding="latin1",
    low_memory=False,
    header=9,          # <-- hier ist der Header
    skip_blank_lines=True
)

# Erste Zeile enthält die echten Spaltennamen -> nach oben „promoten“
df.columns = df.iloc[0]
df = df.iloc[1:].reset_index(drop=True)

# Unbenannte / Gruppen-Spalten wegräumen
df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
df.columns = df.columns.astype(str).str.strip()

print("Shape (clean):", df.shape)
print("Columns (clean):", list(df.columns)[:25], "...")
print(df.head(3))

# Überblick
print("Shape:", df.shape)
print("\nSpaltennamen:")
print(df.columns.tolist())

print("\nErste 5 Zeilen:")
print(df.head())

print("\n✅ Datei wurde erfolgreich geladen!")



# -------------------------------------
# 1️⃣ Datentypen prüfen
print("\nDatentypen:")
print(df.dtypes.head(10))

# -------------------------------------
# 2️⃣ Dezimal-Kommas bereinigen (für kW-Spalten)
for col in df.columns:
    if "kW" in str(col) or "Leistung" in str(col):
        df[col] = (df[col].astype(str)
                           .str.replace(",", ".", regex=False)
                           .str.extract(r"([\d\.]+)")
                           .astype(float))

# -------------------------------------
# 3️⃣ Datum umwandeln
if "Inbetriebnahmedatum" in df.columns:
    df["Inbetriebnahmedatum"] = pd.to_datetime(df["Inbetriebnahmedatum"], dayfirst=True, errors="coerce")

# -------------------------------------
# 4️⃣ Beispielauswertungen

# A) Anzahl Ladeeinrichtungen pro Bundesland
if "Bundesland" in df.columns:
    print("\nTop 10 Bundesländer nach Anzahl Ladeeinrichtungen:")
    print(df["Bundesland"].value_counts().head(10))

# B) Durchschnittliche Nennleistung je Betreiber
pwr_col = next((c for c in df.columns if "Nennleistung Ladeeinrichtung" in str(c) or "kW" in str(c)), None)
if pwr_col and "Betreiber" in df.columns:
    print(f"\nDurchschnittliche Nennleistung je Betreiber (Spalte: {pwr_col}):")
    print(df.groupby("Betreiber")[pwr_col].mean().sort_values(ascending=False).head(10))

# C) Geopunkte prüfen
if {"Breitengrad","Längengrad"}.issubset(df.columns):
    print("\nBeispielhafte Koordinaten:")
    print(df[["Breitengrad","Längengrad"]].head(3))

# -------------------------------------
# 5️⃣ Bereinigte Version speichern
df.to_csv("data/processed_ladesaeulen.csv", index=False)
print("\n💾 Gespeichert als: data/processed_ladesaeulen.csv")




print("\n✅ Datei wurde erfolgreich geladen!")

# -------------------------------------
# 🔍 Visualisierungen
import os
os.makedirs("output", exist_ok=True)

import matplotlib.pyplot as plt

# Top-10 Bundesländer nach Anzahl Ladeeinrichtungen
if "Bundesland" in df.columns:
    top_states = df["Bundesland"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    top_states.plot(kind="bar")
    plt.title("Top 10 Bundesländer nach Anzahl öffentlicher Ladeeinrichtungen")
    plt.xlabel("Bundesland")
    plt.ylabel("Anzahl Ladeeinrichtungen")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("output/ladepunkte_pro_bundesland_top10.png", dpi=150)
    plt.show()

    print("📈 Gespeichert: output/ladepunkte_pro_bundesland_top10.png")
else:
    print("⚠️ Spalte 'Bundesland' nicht gefunden.")



    # Koordinaten bereinigen
lat_col, lon_col = "Breitengrad", "Längengrad"
if {lat_col, lon_col}.issubset(df.columns):
    df[lat_col] = (
        df[lat_col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.extract(r"(-?\d+(?:\.\d+)?)")[0]
        .astype(float)
    )
    df[lon_col] = (
        df[lon_col]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.extract(r"(-?\d+(?:\.\d+)?)")[0]
        .astype(float)
    )

    # Zeilen mit gültigen Koordinaten behalten
    geo = df[[lat_col, lon_col]].dropna()

    # Für Darstellung samplen (sonst werden 97k Punkte sehr dicht)
    sample_n = 5000 if len(geo) > 5000 else len(geo)
    geo_sample = geo.sample(sample_n, random_state=42) if sample_n > 0 else geo

    if len(geo_sample) > 0:
        plt.figure(figsize=(8, 10))
        plt.scatter(geo_sample[lon_col], geo_sample[lat_col], s=3, alpha=0.6)
        plt.title(f"Öffentliche Ladeeinrichtungen in Deutschland (Stichprobe n={len(geo_sample)})")
        plt.xlabel("Längengrad")
        plt.ylabel("Breitengrad")
        plt.tight_layout()
        plt.savefig("output/ladepunkte_scatter_map_sample.png", dpi=150)
        plt.show()

        print("🗺️ Gespeichert: output/ladepunkte_scatter_map_sample.png")
    else:
        print("⚠️ Keine gültigen Koordinaten nach Bereinigung gefunden.")
else:
    print("⚠️ Koordinatenspalten nicht gefunden.")



    # Zeitentwicklung der Inbetriebnahmen
if "Inbetriebnahmedatum" in df.columns:
    # falls noch nicht geschehen:
    df["Inbetriebnahmedatum"] = pd.to_datetime(df["Inbetriebnahmedatum"], dayfirst=True, errors="coerce")
    jahre = df["Inbetriebnahmedatum"].dt.year.dropna().astype(int).value_counts().sort_index()

    if len(jahre) > 0:
        plt.figure(figsize=(10, 5))
        jahre.plot(kind="bar")
        plt.title("Inbetriebnahmen öffentlicher Ladeeinrichtungen pro Jahr")
        plt.xlabel("Jahr")
        plt.ylabel("Anzahl Inbetriebnahmen")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig("output/inbetriebnahmen_pro_jahr.png", dpi=150)
        plt.show()
        print("📅 Gespeichert: output/inbetriebnahmen_pro_jahr.png")