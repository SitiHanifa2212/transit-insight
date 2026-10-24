from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ==================================================
# KONFIGURASI APLIKASI
# ==================================================
st.set_page_config(
    page_title="Transit Insight",
    page_icon="🚌",
    layout="wide",
)

FOLDER = Path(__file__).parent
DATA_PATH = FOLDER / "dashboard_data.csv"

st.title("🚌 Transit Insight")
st.subheader("Dashboard Analisis Transaksi TransJakarta")
st.caption("Integrasi PostgreSQL + SQLite → Pandas → Streamlit + Plotly")

# ==================================================
# MEMUAT DATA CSV — TANPA PASSWORD DATABASE
# ==================================================
@st.cache_data
def muat_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)

    kolom_wajib = [
        "payAmount",
        "durasi_menit",
        "corridorName",
        "tapInTime",
        "tapInStopsName",
        "tapOutStopsName",
    ]

    kolom_hilang = [
        kolom for kolom in kolom_wajib
        if kolom not in data.columns
    ]

    if kolom_hilang:
        raise ValueError(
            "Kolom CSV tidak lengkap: "
            + ", ".join(kolom_hilang)
        )

    data["tapInTime"] = pd.to_datetime(
        data["tapInTime"], errors="coerce"
    )

    if "tapOutTime" in data.columns:
        data["tapOutTime"] = pd.to_datetime(
            data["tapOutTime"], errors="coerce"
        )

    data["tanggal"] = data["tapInTime"].dt.date
    data["jam"] = data["tapInTime"].dt.hour

    for kolom in ["payAmount", "durasi_menit"]:
        data[kolom] = pd.to_numeric(
            data[kolom], errors="coerce"
        )

    return data


try:
    with st.spinner("Memuat data dashboard..."):
        data_asli = muat_data()
except Exception as error:
    st.error("Data dashboard gagal dimuat.")
    st.code(str(error))
    st.stop()

if data_asli.empty:
    st.warning("Tidak ada transaksi untuk ditampilkan.")
    st.stop()

df = data_asli.copy()

# ==================================================
# FILTER SIDEBAR
# ==================================================
with st.sidebar:
    st.header("Filter Dashboard")

    tanggal_tersedia = df["tanggal"].dropna()

    if not tanggal_tersedia.empty:
        tanggal_awal = min(tanggal_tersedia)
        tanggal_akhir = max(tanggal_tersedia)

        rentang = st.date_input(
            "Rentang tanggal",
            value=(tanggal_awal, tanggal_akhir),
            min_value=tanggal_awal,
            max_value=tanggal_akhir,
        )

        if isinstance(rentang, (tuple, list)):
            if len(rentang) == 2:
                mulai, selesai = rentang
                df = df[
                    df["tanggal"].between(mulai, selesai)
                ]
            elif len(rentang) == 1:
                df = df[df["tanggal"] == rentang[0]]

    semua_koridor = sorted(
        df["corridorName"].dropna().unique().tolist()
    )

    pilihan_koridor = st.multiselect(
        "Pilih koridor",
        options=semua_koridor,
        default=semua_koridor,
    )

    df = df[df["corridorName"].isin(pilihan_koridor)]

# ==================================================
# VALIDASI FILTER
# ==================================================
if df.empty:
    st.warning("Tidak ada transaksi yang sesuai dengan filter.")
    st.stop()

st.caption(f"Jumlah data setelah filter: {len(df):,} transaksi")

# ==================================================
# RINGKASAN UTAMA
# ==================================================
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Transaksi", f"{len(df):,}")

total_tarif = df["payAmount"].sum(min_count=1)
k2.metric(
    "Total Nilai Tarif",
    f"Rp {total_tarif:,.0f}"
    if pd.notna(total_tarif) else "N/A",
)

rata_tarif = df["payAmount"].mean()
k3.metric(
    "Rata-rata Tarif",
    f"Rp {rata_tarif:,.0f}"
    if pd.notna(rata_tarif) else "N/A",
)

rata_durasi = df["durasi_menit"].mean()
k4.metric(
    "Rata-rata Durasi",
    f"{rata_durasi:.1f} menit"
    if pd.notna(rata_durasi) else "N/A",
)

st.caption(
    "Nilai tarif merupakan hasil perhitungan dari kolom payAmount "
    "pada dataset, bukan pendapatan resmi TransJakarta."
)

st.divider()

# ==================================================
# TRANSAKSI PER JAM
# ==================================================
kiri, kanan = st.columns(2)

with kiri:
    st.subheader("Pola Transaksi per Jam")

    per_jam = (
        df.dropna(subset=["jam"])
        .groupby("jam")
        .size()
        .reindex(range(24), fill_value=0)
        .rename("Jumlah Transaksi")
        .reset_index()
    )

    fig_jam = px.line(
        per_jam,
        x="jam",
        y="Jumlah Transaksi",
        markers=True,
        title="Jumlah Transaksi Berdasarkan Jam Tap-In",
        labels={"jam": "Jam (0–23)"},
    )

    st.plotly_chart(fig_jam, use_container_width=True)

with kanan:
    st.subheader("10 Koridor Teratas")

    top_koridor = (
        df["corridorName"]
        .dropna()
        .value_counts()
        .head(10)
        .sort_values()
        .rename_axis("Koridor")
        .reset_index(name="Jumlah Transaksi")
    )

    fig_koridor = px.bar(
        top_koridor,
        x="Jumlah Transaksi",
        y="Koridor",
        orientation="h",
        title="Koridor Berdasarkan Jumlah Transaksi",
    )

    st.plotly_chart(fig_koridor, use_container_width=True)

# ==================================================
# HALTE DAN DISTRIBUSI TARIF
# ==================================================
kiri, kanan = st.columns(2)

with kiri:
    st.subheader("10 Halte Tap-In Teratas")

    top_halte = (
        df["tapInStopsName"]
        .dropna()
        .value_counts()
        .head(10)
        .sort_values()
        .rename_axis("Nama Halte")
        .reset_index(name="Jumlah Transaksi")
    )

    fig_halte = px.bar(
        top_halte,
        x="Jumlah Transaksi",
        y="Nama Halte",
        orientation="h",
        title="Halte Berdasarkan Jumlah Tap-In",
    )

    st.plotly_chart(fig_halte, use_container_width=True)

with kanan:
    st.subheader("Distribusi Tarif")

    data_tarif = df.dropna(subset=["payAmount"])

    if not data_tarif.empty:
        fig_tarif = px.histogram(
            data_tarif,
            x="payAmount",
            nbins=20,
            title="Sebaran Nilai Tarif",
            labels={"payAmount": "Nilai Tarif (Rp)"},
        )

        st.plotly_chart(fig_tarif, use_container_width=True)
    else:
        st.info("Tidak ada data tarif yang tersedia.")

# ==================================================
# TABEL TRANSAKSI
# ==================================================
st.divider()
st.subheader("Pratinjau Transaksi")

kolom_tabel = [
    kolom for kolom in [
        "corridorName",
        "tapInStopsName",
        "tapOutStopsName",
        "tapInTime",
        "tapOutTime",
        "durasi_menit",
        "payAmount",
    ]
    if kolom in df.columns
]

st.dataframe(
    df[kolom_tabel].head(100),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Sumber data: dataset transaksi TransJakarta dari Kaggle. "
    "Dashboard menggunakan hasil pipeline yang telah menggabungkan "
    "data transaksi PostgreSQL dan data referensi SQLite menggunakan Pandas."
)
