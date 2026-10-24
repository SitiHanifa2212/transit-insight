
import sqlite3
from pathlib import Path

import pandas as pd

folder_proyek = Path(__file__).parent
file_csv = folder_proyek / "transjakarta_clean.csv"
file_db = folder_proyek / "transit_reference.db"

# Baca data yang sudah dibersihkan
df = pd.read_csv(file_csv)

# Buat tabel referensi koridor
koridor = (
    df[["corridorID", "corridorName"]]
    .dropna(subset=["corridorID", "corridorName"])
    .drop_duplicates()
    .sort_values(["corridorID", "corridorName"])
    .reset_index(drop=True)
)

# Buat referensi halte asal
halte_asal = df[
    [
        "tapInStops",
        "tapInStopsName",
        "tapInStopsLat",
        "tapInStopsLon",
    ]
].copy()

halte_asal.columns = [
    "kode_halte",
    "nama_halte",
    "latitude",
    "longitude",
]

# Buat referensi halte tujuan
halte_tujuan = df[
    [
        "tapOutStops",
        "tapOutStopsName",
        "tapOutStopsLat",
        "tapOutStopsLon",
    ]
].copy()

halte_tujuan.columns = [
    "kode_halte",
    "nama_halte",
    "latitude",
    "longitude",
]

# Gabungkan referensi halte asal dan tujuan
halte = pd.concat(
    [halte_asal, halte_tujuan],
    ignore_index=True,
)

# Buang baris yang tidak memiliki kode atau nama halte
halte = halte.dropna(
    subset=["kode_halte", "nama_halte"]
)

halte = (
    halte.drop_duplicates(
        subset=["kode_halte", "nama_halte"]
    )
    .sort_values(["nama_halte", "kode_halte"])
    .reset_index(drop=True)
)

# Simpan kedua tabel ke SQLite
with sqlite3.connect(file_db) as conn:
    koridor.to_sql(
        "koridor",
        conn,
        if_exists="replace",
        index=False,
    )

    halte.to_sql(
        "halte",
        conn,
        if_exists="replace",
        index=False,
    )

    jumlah_koridor = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM koridor",
        conn,
    ).iloc[0]["total"]

    jumlah_halte = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM halte",
        conn,
    ).iloc[0]["total"]

print("Pembuatan database SQLite berhasil!")
print("File database:", file_db)
print("Jumlah referensi koridor:", jumlah_koridor)
print("Jumlah referensi halte:", jumlah_halte)
