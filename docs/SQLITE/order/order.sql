
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    payment_id INTEGER,
    proposal_id INTEGER,
    status_id INTEGER NOT NULL,
    shipment_status_id INTEGER,
    portal TEXT,
    center TEXT,
    vale_order_id INTEGER UNIQUE NOT NULL,
    besc_order_id INTEGER,
    contract_number TEXT,
    invoice_number TEXT,
    total_value REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (payment_id) REFERENCES payments(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (proposal_id) REFERENCES proposals(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (status_id) REFERENCES orders_status(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (shipment_status_id) REFERENCES shipments(id)
        ON UPDATE CASCADE ON DELETE SET NULL
);