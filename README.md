# Säker Nätverksarkitektur — Gruppuppgift

## Översikt (för lärare)

Denna uppgift simulerar ett överlämningsscenario där ett utvecklingsteam har byggt en applikation och ett DevOps-team ska driftsätta den med fokus på nätverkssäkerhet.

## Struktur

```
SoftwareDevopsTeam/
├── app-repo/              ← Levereras till studenterna som den är
│   ├── app/               ← Flask-applikation med Dockerfile
│   ├── db/                ← Databasschema
│   └── README.md          ← "Från utvecklingsteamet"
│
└── infra-repo/            ← Studenterna forkar detta repo
    ├── docker-compose.yml ← Skelett med TODO:er
    ├── loadbalancer/      ← Skelett med TODO:er
    ├── mariadb/           ← Skelett med TODO:er
    ├── docs/              ← Uppgift, bedömning, ledtrådar
    ├── README.md          ← Studenternas startpunkt
    │
    └── solution/          ← ENBART FÖR LÄRARE
        ├── ...            ← Komplett fungerande lösning
        ├── test.sh        ← Verifieringsskript
        └── ANSWER_KEY.md  ← Lösningskommentarer
```

## Distribuera till studenter

1. **app-repo/** — Ge till alla grupper som den är (t.ex. som ett Git-repo)
2. **infra-repo/** — Ge till studenterna **utan** `solution/`-katalogen

```bash
# Skapa en kopia utan lösningen
rsync -av --exclude='solution' infra-repo/ infra-repo-student/
```

Alternativt, om ni använder Git:

```bash
# Lägg till solution/ i .gitignore innan studenterna får repot
echo "solution/" >> infra-repo/.gitignore
```

## Testa lösningen

```bash
cd infra-repo/solution
docker compose up -d --build

# Vänta ~15 sekunder på att MariaDB startar
sleep 15

# Kör verifieringsskriptet
bash test.sh

# Städa upp
docker compose down -v
```

## Lärandemål

Studenterna övar på:

- **Nätverkssegmentering** med Docker-nätverk
- **Brandväggsregler** med nftables
- **Lastbalansering** med nftables DNAT
- **Principen om minsta privilegium** (databasrättigheter)
- **Docker Compose** med healthchecks, named volumes, IPAM
- **Säkerhetstänk** — varför exponerar vi inte databasen?

## Förkunskaper

Studenterna bör ha grundläggande kunskap om:
- Docker och Docker Compose
- Nätverksprotokoll (TCP/IP)
- SQL
- Linux-kommandon
