
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

st.set_page_config(
    page_title="Transit Insight",
    page_icon="🚌",
    layout="wide",
)

FOLDER = Path(__file__).parent
SQLITE_PATH = FOLDER / "transit_reference.db"

st.title("🚌 Transit Insight")
st.subheader("Dashboard Analisis Transaksi TransJakarta")
st.caption(
    "Integrasi PostgreSQL, SQLite, Pandas, Streamlit, dan Plotly"
)

@st.cache_resource
def buat_engine(password):
    url = URL.create(
        "postgresql+psycopg",
        username="postgres",
        password=password,
        host="127.0.0.1",
        port=5432,
        database="transit_insight",
    )
    return create_engine(url, pool_pre_ping=True)

@st.cache_data(ttl=300)
def muat_data(password):
    engine = buat_engine(password)

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

    with sqlite3.connect(SQLITE_PATH) as conn:
        koridor = pd.read_sql_query(
            "SELECT * FROM koridor", conn
        )
        halte = pd.read_sql_query(
            "SELECT * FROM halte", conn
        )

    data = transaksi.merge(
        koridor,
        on=["corridorID", "corridorName"],
        how="left",
        validate="many_to_one",
    )

    halte_unik = (
        halte.dropna(subset=["kode_halte"])
        .drop_duplicates(subset=["kode_halte"])
    )

    data = data.merge(
        halte_unik[["kode_halte", "latitude", "longitude"]],
        left_on="tapInStops",
        right_on="kode_halte",
        how="left",
        validate="many_to_one",
    )

    data["tapInTime"] = pd.to_datetime(
        data["tapInTime"], errors="coerce"
    )
    data["tanggal"] = data["tapInTime"].dt.date
    data["jam"] = data["tapInTime"].dt.hour
    data["payAmount"] = pd.to_numeric(
        data["payAmount"], errors="coerce"
    )
    data["durasi_menit"] = pd.to_numeric(
        data["durasi_menit"], errors="coerce"
    )

    return data

with st.sidebar:
    st.header("Koneksi Database")
    password = st.text_input(
        "Password PostgreSQL",
        type="password",
    )
    st.caption("Masukkan password PostgreSQL lokal.")

if not password:
    st.info(
        "Masukkan password PostgreSQL di sidebar untuk "
        "memuat dashboard."
    )
    st.stop()

if not SQLITE_PATH.exists():
    st.error("File transit_reference.db tidak ditemukan.")
    st.stop()

try:
    with st.spinner("Mengambil data dari kedua database..."):
        df = muat_data(password)
except Exception as error:
    st.error(
        "Data gagal dimuat. Periksa password, status PostgreSQL, "
        "dan struktur tabel database."
    )
    st.code(str(error))
    st.stop()

if df.empty:
    st.warning("Tidak ada transaksi untuk ditampilkan.")
    st.stop()

with st.sidebar:
    st.divider()
    st.header("Filter")

    tanggal_tersedia = df["tanggal"].dropna()

    if not tanggal_tersedia.empty:
        tanggal = st.date_input(
            "Rentang tanggal",
            value=(
                min(tanggal_tersedia),
                max(tanggal_tersedia),
            ),
            min_value=min(tanggal_tersedia),
            max_value=max(tanggal_tersedia),
        )

        if isinstance(tanggal, (tuple, list)) and len(tanggal) == 2:
            df = df[df["tanggal"].between(tanggal[0], tanggal[1])]

    semua_koridor = sorted(
        df["corridorName"].dropna().unique().tolist()
    )

    pilihan = st.multiselect(
        "Koridor",
        options=semua_koridor,
        default=semua_koridor,
    )

    df = df[df["corridorName"].isin(pilihan)]

if df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter.")
    st.stop()

# Ringkasan
st.caption(f"Jumlah data setelah filter: {len(df):,} transaksi")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Transaksi", f"{len(df):,}")

tarif_total = df["payAmount"].sum(min_count=1)
k2.metric(
    "Total Nilai Tarif",
    f"Rp {tarif_total:,.0f}"
    if pd.notna(tarif_total) else "N/A",
)

tarif_rata = df["payAmount"].mean()
k3.metric(
    "Rata-rata Tarif",
    f"Rp {tarif_rata:,.0f}"
    if pd.notna(tarif_rata) else "N/A",
)

durasi_rata = df["durasi_menit"].mean()
k4.metric(
    "Rata-rata Durasi",
    f"{durasi_rata:.1f} menit"
    if pd.notna(durasi_rata) else "N/A",
)

st.caption(
    "Total nilai tarif dihitung dari nilai payAmount yang tersedia, "
    "bukan klaim pendapatan resmi TransJakarta."
)

st.divider()

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
        labels={
            "jam": "Jam (0–23)",
            "Jumlah Transaksi": "Jumlah Transaksi",
        },
    )
    st.plotly_chart(fig_jam, use_container_width=True)

with kanan:
    st.subheader("10 Koridor Teratas")

    top = (
        df["corridorName"]
        .dropna()
        .value_counts()
        .head(10)
        .sort_values()
        .rename_axis("Koridor")
        .reset_index(name="Jumlah Transaksi")
    )

    fig_top = px.bar(
        top,
        x="Jumlah Transaksi",
        y="Koridor",
        orientation="h",
        title="Koridor Berdasarkan Jumlah Transaksi",
    )
    st.plotly_chart(fig_top, use_container_width=True)

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

    tarif = df.dropna(subset=["payAmount"])

    if not tarif.empty:
        fig_tarif = px.histogram(
            tarif,
            x="payAmount",
            nbins=20,
            title="Sebaran Nilai Tarif",
            labels={"payAmount": "Nilai Tarif (Rp)"},
        )
        st.plotly_chart(fig_tarif, use_container_width=True)
    else:
        st.info("Tidak ada data tarif yang tersedia.")

st.divider()
st.subheader("Pratinjau Transaksi")

kolom = [
    "corridorName",
    "tapInStopsName",
    "tapOutStopsName",
    "tapInTime",
    "tapOutTime",
    "durasi_menit",
    "payAmount",
]

st.dataframe(
    df[kolom].head(100),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Sumber: dataset transaksi TransJakarta dari Kaggle. "
    "Data referensi koridor dan halte berasal dari pengolahan dataset "
    "yang sama ke dalam SQLite."
)
