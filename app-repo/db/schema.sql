CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO items (name, description) VALUES
    ('Laptop', 'En bärbar dator med 16GB RAM'),
    ('Tangentbord', 'Mekaniskt tangentbord med RGB-belysning'),
    ('Bildskärm', '27-tums 4K-bildskärm');
