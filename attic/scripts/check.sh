#!/bin/bash
export FLY_NO_UPDATE_CHECK=1
export HTTPS_PROXY=http://127.0.0.1:8080
export HTTP_PROXY=http://127.0.0.1:8080
export SSL_CERT_FILE=/data/data/com.termux/files/usr/etc/tls/cert.pem

echo "=== LOCAL POND ==="
ps aux | grep -E "pond_daemon|proxy.py" | grep -v grep

echo ""
echo "=== FLY WITNESS ==="
~/.fly/bin/flyctl status -a pond-fly-witness 2>&1 | tail -10

echo ""
echo "=== API ==="
curl -s https://pond-fly-witness.fly.dev/ && echo
