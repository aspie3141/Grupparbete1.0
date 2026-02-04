# Infrastruktur-repo — Säker Nätverksarkitektur

## Översikt

Detta repo innehåller infrastrukturkonfigurationen för att driftsätta en Flask-applikation med fokus på säkerhet. Er uppgift är att fylla i de filer som är markerade med `TODO`.

Applikationskoden finns i `app-repo/` (separat repo) — den ska ni **inte ändra**.

## Struktur

```
infra-repo/
├── docker-compose.yml           ← Fyll i TODO:er
├── loadbalancer/
│   ├── Dockerfile               ← Klar (behöver inte ändras)
│   ├── nftables.conf            ← Fyll i nftables-regler
│   └── entrypoint.sh            ← Fyll i startskript
├── mariadb/
│   └── init.sql                 ← Fyll i tabell, användare, rättigheter
└── docs/
    ├── ASSIGNMENT.md            ← Fullständig uppgiftsbeskrivning
    ├── GRADING.md               ← Bedömningsmatris (G/VG)
    └── HINTS.md                 ← Ledtrådar (använd vid behov)
```

## Kom igång

1. Läs igenom `docs/ASSIGNMENT.md` noggrant
2. Studera applikationens README i `app-repo/README.md`
3. Börja med `docker-compose.yml` — det är grunden
4. Fortsätt med `mariadb/init.sql`
5. Konfigurera lastbalanseraren (`loadbalancer/`)
6. Testa allt med kommandona i uppgiftsbeskrivningen

## Filer att redigera

| Fil | Vad ska göras |
|-----|---------------|
| `docker-compose.yml` | Definiera nätverk, volymer, miljövariabler, portar |
| `loadbalancer/nftables.conf` | Skriv nftables-regler för lastbalansering och filtrering |
| `loadbalancer/entrypoint.sh` | Skriv startskript (ip_forward, nft, keep-alive) |
| `mariadb/init.sql` | Skapa tabell, seed data, användare med begränsade rättigheter |

## Krav

- Docker och Docker Compose installerat
- `app-repo/` ska finnas i samma överordnade katalog som `infra-repo/`

## Dokumentation

Se `docs/`-katalogen:
- **ASSIGNMENT.md** — Fullständig uppgiftsbeskrivning med arkitekturdiagram
- **GRADING.md** — Bedömningsmatris för G och VG
- **HINTS.md** — Progressiva ledtrådar om ni kör fast
