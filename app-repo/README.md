# Inventariehantering API

## Från utvecklingsteamet till DevOps-teamet

Hej DevOps!

Vi har byggt klart ett REST API för inventariehantering. Nu är det er tur att sätta upp infrastrukturen. Nedan hittar ni all information ni behöver för att driftsätta applikationen.

## Endpoints

| Metod | Sökväg | Beskrivning |
|-------|--------|-------------|
| GET | `/items` | Hämta alla objekt |
| GET | `/items/{id}` | Hämta ett specifikt objekt |
| POST | `/items` | Skapa ett nytt objekt |
| PUT | `/items/{id}` | Uppdatera ett objekt |
| GET | `/health` | Hälsokontroll |

**Obs:** DELETE och HEAD är inte implementerade och returnerar 405.

## Svarsformat

Alla svar innehåller `hostname` för att identifiera vilken instans som hanterade anropet:

```json
{
    "hostname": "app1",
    "data": { ... }
}
```

## Miljövariabler

Applikationen konfigureras med följande miljövariabler:

| Variabel | Beskrivning | Standardvärde |
|----------|-------------|---------------|
| `DB_HOST` | Databasvärd | `mariadb` |
| `DB_PORT` | Databasport | `3306` |
| `DB_USER` | Databasanvändare | `app_user` |
| `DB_PASSWORD` | Databaslösenord | `secure_password_123` |
| `DB_NAME` | Databasnamn | `app_db` |

## Port

Applikationen lyssnar på **port 5000**.

## Bygga och köra

```bash
# Bygga Docker-image
docker build -t inventory-api app/

# Köra container (kräver en tillgänglig MariaDB)
docker run -p 5000:5000 \
  -e DB_HOST=mariadb \
  -e DB_USER=app_user \
  -e DB_PASSWORD=secure_password_123 \
  -e DB_NAME=app_db \
  inventory-api
```

## Databas

SQL-schemat finns i `db/schema.sql`. Det skapar tabellen `items` och lägger in tre exempelrader. Ni behöver själva se till att:

1. En MariaDB-instans körs och är tillgänglig
2. Schemat laddas in vid uppstart
3. En databasanvändare med lämpliga rättigheter skapas

## Beroenden

- Python 3.11
- Flask
- PyMySQL

Lycka till!
*— Utvecklingsteamet*
