
-- ==============================
-- Table: ICMS TAXES
-- ==============================
CREATE TABLE IF NOT EXISTS icms(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value REAL,
    rate REAL,
    base_amount REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);



