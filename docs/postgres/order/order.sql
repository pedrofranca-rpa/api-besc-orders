CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    
    customer_id INTEGER NOT NULL,
    payment_id INTEGER NOT NULL,
    status_id INTEGER DEFAULT 0,
    vale_order_id BIGINT NOT NULL UNIQUE,
    besc_order_id BIGINT UNIQUE,
    total_value NUMERIC(12, 2) NOT NULL,

    state VARCHAR(3),
    portal VARCHAR(50),
    center VARCHAR(100),
    contract_number VARCHAR(100),
    invoice_number VARCHAR(50),

    proposal_id INTEGER,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT fk_orders_customer_id
        FOREIGN KEY (customer_id)
        REFERENCES customers (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_orders_payment_id
        FOREIGN KEY (payment_id)
        REFERENCES payments (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_orders_status_id
        FOREIGN KEY (status_id)
        REFERENCES orders_status (id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_orders_proposal_id
        FOREIGN KEY (proposal_id)
        REFERENCES proposals (id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);
