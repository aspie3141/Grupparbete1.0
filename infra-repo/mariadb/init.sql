-- =============================================================
-- Databasinitiering
-- =============================================================

-- TODO: Skapa tabellen "items" med följande kolumner:
--   id          - INT, auto-increment, primärnyckel
--   name        - VARCHAR(255), NOT NULL
--   description - TEXT
--   created_at  - TIMESTAMP med standardvärde CURRENT_TIMESTAMP


-- TODO: Lägg in exempeldata (minst 3 rader)
-- INSERT INTO items (name, description) VALUES ...


-- TODO: Skapa en databasanvändare för applikationen
-- Användaren ska ha BEGRÄNSADE rättigheter (principen om minsta privilegium)
-- Tips: Fundera på vilka SQL-operationer applikationen faktiskt behöver.
--       Vilka operationer stöder API:et? (Titta på endpoints i app-repo)
--       Behöver applikationen kunna radera data?
--
-- CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY '...';
-- GRANT ... ON app_db.* TO 'app_user'@'%';
-- FLUSH PRIVILEGES;
