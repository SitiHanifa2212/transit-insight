
import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Lokasi file CSV hasil pembersihan
file_csv = Path(__file__).parent / "transjakarta_clean.csv"

if not file_csv.exists():
    raise FileNotFoundError(
        f"File tidak ditemukan: {file_csv}"
    )

# Baca data
df = pd.read_csv(file_csv)

# Minta password secara aman; password tidak disimpan di kode
password = getpass.getpass("Masukkan password PostgreSQL: ")

# Buat koneksi PostgreSQL
url = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password=password,
    host="127.0.0.1",
    port=5432,
    database="transit_insight",
)

engine = create_engine(url)

try:
    # Uji koneksi
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    print("Koneksi PostgreSQL berhasil!")
    print("Jumlah data yang akan diimpor:", len(df))

    # Impor data ke tabel transaksi
    df.to_sql(
        name="transaksi",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )

    # Verifikasi jumlah data di database
    with engine.connect() as conn:
        jumlah = conn.execute(
            text("SELECT COUNT(*) FROM transaksi")
        ).scalar_one()

    print("Impor selesai!")
    print("Jumlah baris dalam PostgreSQL:", jumlah)
    print("Nama tabel: transaksi")

finally:
    engine.dispose()
