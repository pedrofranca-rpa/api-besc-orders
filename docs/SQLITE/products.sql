
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    tax_id INTEGER,
    part_number TEXT,
    description TEXT,
    ncm_code TEXT,
    unit TEXT,
    quantity INTEGER DEFAULT 0,
    unit_price REAL DEFAULT 0,
    material TEXT,
    origin TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (tax_id) REFERENCES tax(id)
        ON UPDATE CASCADE ON DELETE SET NULL
);