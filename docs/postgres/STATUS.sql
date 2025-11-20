
-- Table: order_status
CREATE TABLE IF NOT EXISTS orders_status (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

INSERT INTO orders_status (id, name)
VALUES 
    (1, 'OK'),
    (2, 'Pendente')
ON CONFLICT (id) DO NOTHING;


-- Table: ticket_status
CREATE TABLE IF NOT EXISTS tickets_status (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Table: proposal_status (NEW!)
CREATE TABLE IF NOT EXISTS proposals_status (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Table: shipment_status (NEW!)
CREATE TABLE IF NOT EXISTS shipments_status (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

