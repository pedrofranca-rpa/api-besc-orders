CREATE TABLE IF NOT EXISTS shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status_id INTEGER,
    name TEXT NOT NULL,
    tracking_number TEXT,
    shipment_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (status_id) REFERENCES shipment_status(id)
        ON UPDATE CASCADE ON DELETE SET NULL
);