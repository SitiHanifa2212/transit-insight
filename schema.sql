-- Transit Insight
-- DDL untuk membuat tabel transaksi di database PostgreSQL.
-- Jalankan setelah database transit_insight dibuat.
--
-- Catatan:
-- 1. Sesuaikan tipe/nama kolom jika berbeda dari transjakarta_clean.csv.
-- 2. Script impor_postgres.py saat ini memakai pandas.to_sql(if_exists="replace"),
--    sehingga akan mengganti tabel ini ketika script impor dijalankan.
-- 3. Jalankan di database transit_insight, bukan di database postgres default.

CREATE TABLE IF NOT EXISTS transaksi (
    "transID" TEXT,
    "corridorID" TEXT,
    "corridorName" TEXT,
    "direction" TEXT,
    "tapInStops" TEXT,
    "tapInStopsName" TEXT,
    "tapInLat" DOUBLE PRECISION,
    "tapInLon" DOUBLE PRECISION,
    "tapOutStops" TEXT,
    "tapOutStopsName" TEXT,
    "tapOutLat" DOUBLE PRECISION,
    "tapOutLon" DOUBLE PRECISION,
    "stopSequence" INTEGER,
    "tapInTime" TIMESTAMP,
    "tapOutTime" TIMESTAMP,
    "payAmount" NUMERIC(12, 2),
    "durasi_menit" DOUBLE PRECISION
);

-- Indeks opsional untuk membantu pencarian berdasarkan waktu dan koridor.
CREATE INDEX IF NOT EXISTS idx_transaksi_tapintime
    ON transaksi ("tapInTime");

CREATE INDEX IF NOT EXISTS idx_transaksi_corridorid
    ON transaksi ("corridorID");
