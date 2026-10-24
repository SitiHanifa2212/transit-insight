
import getpass
import sqlite3
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

folder = Path(__file__).parent
sqlite_path = folder / "transit_reference.db"

password = getpass.getpass("Password PostgreSQL: ")

url = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password=password,
    host="127.0.0.1",
    port=5432,
    database="transit_insight",
)

engine = create_engine(url)

try:
    with engine.connect() as conn:
        transaksi = pd.read_sql_query(
            text("""
                SELECT
                    "transID",
                    "corridorID",
                    "corridorName",
                    "tapInStops",
                    "tapInStopsName",
                    "tapOutStops",
                    "tapOutStopsName",
                    "tapInTime",
                    "tapOutTime",
                    "payAmount",
                    durasi_menit
                FROM transaksi
            """),
            conn,
        )
    print("Data PostgreSQL:", len(transaksi), "baris")

    with sqlite3.connect(sqlite_path) as conn:
        koridor = pd.read_sql_query(
            "SELECT * FROM koridor", conn
        )
        halte = pd.read_sql_query(
            "SELECT * FROM halte", conn
        )

    print("Referensi koridor SQLite:", len(koridor))
    print("Referensi halte SQLite:", len(halte))

    gabungan = transaksi.merge(
        koridor,
        on=["corridorID", "corridorName"],
        how="left",
        validate="many_to_one",
    )

    halte_unik = (
        halte.dropna(subset=["kode_halte"])
        .drop_duplicates(subset=["kode_halte"])
    )

    gabungan = gabungan.merge(
        halte_unik[["kode_halte", "latitude", "longitude"]],
        left_on="tapInStops",
        right_on="kode_halte",
        how="left",
        validate="many_to_one",
    )

    print("\n=== HASIL PIPELINE ===")
    print("Jumlah baris hasil merge:", len(gabungan))
    print(
        "Koordinat halte terisi:",
        gabungan["latitude"].notna().sum(),
    )

    print("\nContoh hasil:")
    print(
        gabungan[
            [
                "transID",
                "corridorName",
                "tapInStopsName",
                "latitude",
                "longitude",
                "payAmount",
            ]
        ].head().to_string(index=False)
    )

    output = folder / "hasil_pipeline.csv"
    gabungan.to_csv(output, index=False)
    print("\nFile hasil:", output)

finally:
    engine.dispose()
