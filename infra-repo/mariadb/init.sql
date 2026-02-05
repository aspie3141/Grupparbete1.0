-- =============================================================
-- Databasinitiering
-- =============================================================

-- Skapa tabellen "items"
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lägg in exempeldata
INSERT INTO items (name, description) VALUES 
    ('Artikel 1', 'En beskrivning av artikel 1'),
    ('Artikel 2', 'En beskrivning av artikel 2'),
    ('Artikel 3', 'En beskrivning av artikel 3');

-- Skapa en databasanvändare för applikationen med minsta privilegium
-- Applikationen behöver: SELECT, INSERT, UPDATE (ej DELETE)
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'secure_password_123';
GRANT SELECT, INSERT, UPDATE ON app_db.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
