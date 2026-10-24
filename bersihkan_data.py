
import pandas as pd
from pathlib import Path

# Lokasi dataset asli
file_csv = (
    Path.home()
    / "Downloads"
    / "dfTransjakarta.csv"
    / "dfTransjakarta.csv"
)

# Baca dataset
df = pd.read_csv(file_csv)

# Pilih kolom yang relevan untuk analisis perjalanan
kolom_analisis = [
    "transID",
    "corridorID",
    "corridorName",
    "direction",
    "tapInStops",
    "tapInStopsName",
    "tapInStopsLat",
    "tapInStopsLon",
    "stopStartSeq",
    "tapInTime",
    "tapOutStops",
    "tapOutStopsName",
    "tapOutStopsLat",
    "tapOutStopsLon",
    "stopEndSeq",
    "tapOutTime",
    "payAmount",
]

data = df[kolom_analisis].copy()

# Ubah kolom waktu menjadi format tanggal/waktu
data["tapInTime"] = pd.to_datetime(
    data["tapInTime"], errors="coerce"
)
data["tapOutTime"] = pd.to_datetime(
    data["tapOutTime"], errors="coerce"
)

# Hitung durasi perjalanan dalam menit
data["durasi_menit"] = (
    data["tapOutTime"] - data["tapInTime"]
).dt.total_seconds() / 60

# Simpan hasil di folder proyek
output = Path(__file__).parent / "transjakarta_clean.csv"
data.to_csv(output, index=False)

print("Pembersihan data selesai!")
print("Jumlah baris:", len(data))
print("Jumlah kolom:", len(data.columns))
print("File hasil:", output)
print("\nJumlah nilai kosong per kolom:")
print(data.isnull().sum().to_string())
