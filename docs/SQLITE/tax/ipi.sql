-- ==============================
-- Table: IPI TAXES
-- ==============================
CREATE TABLE IF NOT EXISTS ipi(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value REAL,
    rate REAL,
    base_amount REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);