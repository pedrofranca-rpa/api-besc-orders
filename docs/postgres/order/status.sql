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
