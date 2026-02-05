#!/bin/sh

# =============================================================
# Startskript för lastbalanseraren
# =============================================================

# Aktivera IP-forwarding (försöker, men ignorerar fel om /proc är read-only)
echo 1 > /proc/sys/net/ipv4/ip_forward 2>/dev/null || true

# Ladda nftables-konfigurationen
nft -f /etc/nftables.conf

echo "Lastbalanserare startad."

# Håll containern igång
tail -f /dev/null
