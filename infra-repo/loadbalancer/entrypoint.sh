#!/bin/sh

# =============================================================
# Startskript för lastbalanseraren
# =============================================================

# TODO: Aktivera IP-forwarding
# Tips: Skriv värdet 1 till /proc/sys/net/ipv4/ip_forward
# echo ...

# TODO: Ladda nftables-konfigurationen
# Tips: Använd "nft -f" med sökvägen till konfigurationsfilen
# nft ...

echo "Lastbalanserare startad."

# TODO: Håll containern igång
# Tips: Containern avslutas om denna process avslutas.
# Använd ett kommando som körs för evigt, t.ex. tail -f /dev/null
