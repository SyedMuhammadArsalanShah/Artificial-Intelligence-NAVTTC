CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO users (name, email) VALUES
('Nawaira', 'nawaira@example.com'),
('Laiba', 'laiba@example.com'),
('Mufti Sahab', 'muftisahab@example.com'),
('Usman FAV Student', 'usman@example.com');