
import pandas as pd
from pathlib import Path

file_csv = Path.home() / "Downloads" / "dfTransjakarta.csv" / "dfTransjakarta.csv"

if not file_csv.exists():
    print("File CSV tidak ditemukan:", file_csv)
    raise SystemExit

df = pd.read_csv(file_csv)

print("\n=== PEMERIKSAAN DATA TRANSJAKARTA ===")
print("Lokasi file:", file_csv)
print("Jumlah baris:", len(df))
print("Jumlah kolom:", len(df.columns))

print("\n=== NAMA KOLOM ===")
for kolom in df.columns:
    print("-", kolom)

print("\n=== LIMA BARIS PERTAMA ===")
print(df.head().to_string())

print("\n=== JUMLAH DATA KOSONG ===")
print(df.isnull().sum().to_string())

print("\n=== TIPE DATA ===")
print(df.dtypes.to_string())
