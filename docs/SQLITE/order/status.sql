CREATE TABLE IF NOT EXISTS orders_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL
);

INSERT INTO orders_status (id, name)
VALUES 
    (1, 'Pendente'),
    (2, 'OK')
ON CONFLICT (id) DO NOTHING;