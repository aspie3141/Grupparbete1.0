# Gruppuppgift: Säker Nätverksarkitektur med Docker

## Scenario

Ni arbetar som DevOps-team på ett företag. Utvecklingsteamet har byggt klart ett REST API (en Flask-applikation) och lämnat över det till er. Er uppgift är att driftsätta applikationen med fokus på **säkerhet, tillgänglighet och nätverkssegmentering**.

Applikationen finns i `app-repo/` och ni ska **inte ändra applikationskoden**. Ert arbete sker i `infra-repo/`.

## Arkitektur

```
                    ┌─────────────────────────────────────────────────┐
                    │              frontend (172.20.0.0/24)           │
                    │                                                 │
   Port 80         │  ┌──────────┐    ┌──────┐     ┌──────┐         │
  ─────────────────►│  │    LB    │───►│ app1 │     │ app2 │         │
  Användare         │  │ nftables │───►│:5000 │     │:5000 │         │
                    │  │ .0.10    │    │.0.11 │     │.0.12 │         │
                    │  └──────────┘    └──┬───┘     └──┬───┘         │
                    │                     │            │              │
                    └─────────────────────┼────────────┼──────────────┘
                                          │            │
                    ┌─────────────────────┼────────────┼──────────────┐
                    │              backend │            │              │
                    │                 ┌────┴────────────┴───┐         │
                    │                 │      MariaDB         │         │
                    │                 │     (port 3306)      │         │
                    │                 └─────────────────────┘         │
                    └─────────────────────────────────────────────────┘
```

**Viktigt:** Lastbalanseraren ska **inte** kunna nå databasen direkt.

## Krav

### 1. Docker Compose (`docker-compose.yml`)

Skapa en komplett `docker-compose.yml` som definierar:

- **Lastbalanserare** (`loadbalancer`)
  - Bygger från `./loadbalancer`
  - Exponerar port 80
  - Har `NET_ADMIN` capability (krävs för nftables)
  - Aktiverar IP-forwarding via sysctls
  - Ansluten till `frontend`-nätverket med IP `172.20.0.10`

- **Två applikationsinstanser** (`app1` och `app2`)
  - Bygger från `../app-repo/app`
  - Konfigurerade med miljövariabler för databasanslutning
  - Anslutna till **både** `frontend` och `backend`
  - Statiska IP:er: `172.20.0.11` (app1) och `172.20.0.12` (app2)
  - Startar först när databasen är klar (healthcheck)

- **Databas** (`mariadb`)
  - Använder `mariadb:10`
  - Ansluten **enbart** till `backend`-nätverket
  - Ingen port exponerad mot hosten
  - Healthcheck konfigurerad
  - Persistent lagring via named volume

- **Nätverk**
  - `frontend`: bridge med IPAM-subnet `172.20.0.0/24`
  - `backend`: bridge

### 2. Lastbalanserare (`loadbalancer/`)

Konfigurera nftables-baserad lastbalansering:

- **`nftables.conf`**: Regler för round-robin-lastbalansering som fördelar trafik på port 80 mellan `app1` och `app2` på port 5000
- **`entrypoint.sh`**: Startskript som aktiverar IP-forwarding, laddar nftables-regler och håller containern igång

### 3. Databassäkerhet (`mariadb/init.sql`)

- Skapa tabellstruktur och exempeldata
- Skapa en applikationsanvändare med **begränsade rättigheter**
- Tillämpa principen om minsta privilegium

### 4. Nätverkssegmentering

- Databasen ska **enbart** finnas på backend-nätverket
- Lastbalanseraren ska **inte** kunna kommunicera med databasen
- Applikationsservrarna fungerar som brygga mellan frontend och backend

## Säkerhetskrav

| Krav | Beskrivning |
|------|-------------|
| Nätverkssegmentering | Databasen isolerad på backend-nätverk |
| Brandväggsregler | nftables med policy drop, bara nödvändig trafik tillåts |
| Minsta privilegium | Databasanvändaren har bara de rättigheter som behövs |
| Ingen exponering | Databasen har inga portar exponerade mot hosten |
| Tillgänglighet | Lastbalansering över två instanser |

## Leverabler

1. **Fungerande infrastruktur** — `docker compose up -d --build` ska starta hela miljön
2. **Verifierad funktionalitet:**
   - Alla API-endpoints fungerar via port 80
   - Lastbalansering fördelar trafik (kontrollera `hostname` i svar)
   - `DELETE`-anrop returnerar 405
   - Databasen är inte nåbar från lastbalanseraren
3. **Dokumentation** — Kort beskrivning av era val och hur ni verifierat säkerheten

## Testa er lösning

```bash
# Starta miljön
docker compose up -d --build

# Testa endpoints (kör flera gånger — hostname ska variera)
curl http://localhost/items
curl http://localhost/items

# Skapa nytt objekt
curl -X POST http://localhost/items \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test", "description": "Testrrad"}'

# Uppdatera objekt
curl -X PUT http://localhost/items/1 \
  -H 'Content-Type: application/json' \
  -d '{"name": "Uppdaterad"}'

# Verifiera att DELETE inte fungerar (ska ge 405)
curl -X DELETE http://localhost/items/1

# Hälsokontroll
curl http://localhost/health

# Verifiera nätverksisolering
docker exec loadbalancer ping -c 1 mariadb    # Ska misslyckas!
docker exec app1 ping -c 1 mariadb            # Ska lyckas

# Verifiera databasrättigheter
docker exec mariadb mysql -u app_user -psecure_password_123 \
  -e "DELETE FROM items WHERE id=1" app_db     # Ska misslyckas!

# Stoppa miljön
docker compose down -v
```
