CREATE TABLE IF NOT EXISTS transaksi (
    "transID" TEXT,
    "corridorID" TEXT,
    "corridorName" TEXT,
    "direction" INTEGER,
    "tapInStops" TEXT,
    "tapInStopsName" TEXT,
    "tapInStopsLat" DOUBLE PRECISION,
    "tapInStopsLon" DOUBLE PRECISION,
    "stopStartSeq" DOUBLE PRECISION,
    "tapInTime" TIMESTAMP,
    "tapOutStops" TEXT,
    "tapOutStopsName" TEXT,
    "tapOutStopsLat" DOUBLE PRECISION,
    "tapOutStopsLon" DOUBLE PRECISION,
    "stopEndSeq" DOUBLE PRECISION,
    "tapOutTime" TIMESTAMP,
    "payAmount" NUMERIC(12, 2),
    "durasi_menit" DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS idx_transaksi_tapintime
    ON transaksi ("tapInTime");

CREATE INDEX IF NOT EXISTS idx_transaksi_corridorid
    ON transaksi ("corridorID");
