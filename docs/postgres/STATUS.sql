
-- Table: order_statuses
CREATE TABLE IF NOT EXISTS orders_statuses (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Table: ticket_statuses
CREATE TABLE IF NOT EXISTS tickets_statuses (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Table: proposal_statuses (NEW!)
CREATE TABLE IF NOT EXISTS proposals_statuses (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

-- Table: shipment_statuses (NEW!)
CREATE TABLE IF NOT EXISTS shipments_statuses (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

