-- Table-PT: CLIENTES
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tax_id VARCHAR(20),  -- CNPJ/CPF
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table-PT: EXPEDICAO
CREATE TABLE IF NOT EXISTS shipments (
    id SERIAL PRIMARY KEY,
    status_id INTEGER REFERENCES shipment_status(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    name TEXT NOT NULL,
    tracking_number TEXT,
    shipment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table-PT: PROPOSTAS
CREATE TABLE IF NOT EXISTS proposals (
    id SERIAL PRIMARY KEY,
    proposal_number INTEGER UNIQUE,
    status_id INTEGER REFERENCES proposal_status(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    payment_date DATE,
    billing_until DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table-PT: PEDIDOS
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    proposal_id INTEGER REFERENCES proposals(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    status_id INTEGER NOT NULL REFERENCES order_status(id)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    shipment_status_id INTEGER REFERENCES shipment(id)
        ON UPDATE CASCADE ON DELETE SET NULL,

    portal VARCHAR(50),
    center VARCHAR(100),
    vale_order_id INTEGER UNIQUE NOT NULL,
    besc_order_id INTEGER,
    contract_number VARCHAR(100),
    billing_due_date DATE,
    delivery_date DATE,
    invoice_number VARCHAR(50),
    total_value NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table-PT: support_tickets
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    ticket_number INTEGER,
    opened_at DATE,
    closed_at DATE,
    status_id INTEGER REFERENCES tickets_status(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table-PT: icms_taxes
CREATE TABLE IF NOT EXISTS icms (
    id SERIAL PRIMARY KEY,
    value NUMERIC(10,2),
    rate NUMERIC(5,2),
    base_amount NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table-PT: ipi_taxes
CREATE TABLE IF NOT EXISTS ipi (
    id SERIAL PRIMARY KEY,
    value NUMERIC(10,2),
    rate NUMERIC(5,2),
    base_amount NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table-PT: tax_records
CREATE TABLE IF NOT EXISTS tax (
    id SERIAL PRIMARY KEY,
    icms_id INTEGER REFERENCES icms_taxes(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    ipi_id INTEGER REFERENCES ipi_taxes(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table-PT: order_items
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    tax_record_id INTEGER REFERENCES tax_records(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    part_number VARCHAR(50),
    description TEXT,
    ncm_code VARCHAR(20),
    unit VARCHAR(10),
    quantity INTEGER DEFAULT 0,
    unit_price NUMERIC(12,2) DEFAULT 0,
    material VARCHAR(50),
    origin VARCHAR(50),
    total_price NUMERIC(14,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);