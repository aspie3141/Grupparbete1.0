FROM alpine:3.19

RUN apk add --no-cache nftables

COPY nftables.conf /etc/nftables.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && ls -la /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]