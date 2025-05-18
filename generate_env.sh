#!/usr/bin/env bash
sudo apt update && sudo apt install -y jq openssl
set -eu

# Этот скрипт нужно запускать из корня проекта, где лежат:
# ./xui/config.json, ./wg-portal/config/config.yaml и docker-compose.yml

ENV_FILE=".env"
echo "# Автосгенерированный .env" > "$ENV_FILE"

### X-UI ###
echo -e "\n# X-UI (VLESS/Reality)" >> "$ENV_FILE"
echo "XUI_BASE_URL=http://xui:54321" >> "$ENV_FILE"

# получаем из переменных окружения контейнера xui
XUI_USERNAME=$(docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' xui \
  | grep '^XUI_WEB_USERNAME=' | cut -d= -f2-)
XUI_PASSWORD=$(docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' xui \
  | grep '^XUI_WEB_PASSWORD=' | cut -d=-)
echo "XUI_USERNAME=$XUI_USERNAME" >> "$ENV_FILE"
echo "XUI_PASSWORD=$XUI_PASSWORD" >> "$ENV_FILE"

# inbound ID берём из локального конфига
if [[ -f ./xui/config.json ]]; then
  INBOUND_ID=$(jq -r '.inbounds[] | select(.protocol=="vless") .id' ./xui/config.json)
else
  INBOUND_ID=""
fi
echo "XUI_INBOUND_ID=$INBOUND_ID" >> "$ENV_FILE"

### Pritunl (OpenVPN) ###
echo -e "\n# Pritunl (OpenVPN)" >> "$ENV_FILE"
# обычно PRITUNL_BASE_URL = ваш публичный домен
echo "PRITUNL_BASE_URL=https://vpn.testdomain.su" >> "$ENV_FILE"
# токен/секрет/ID org нужно вставить вручную после просмотра в UI
echo "PRITUNL_API_TOKEN=" >> "$ENV_FILE"
echo "PRITUNL_API_SECRET=" >> "$ENV_FILE"
echo "PRITUNL_ORG_ID=" >> "$ENV_FILE"

### Outline (Shadowbox) ###
echo -e "\n# Outline (Shadowbox)" >> "$ENV_FILE"
echo "OUTLINE_API_URL=https://vpn.testdomain.su/outline" >> "$ENV_FILE"
# вычисляем SHA256 отпечаток TLS-сертификата вашего домена
if command -v openssl >/dev/null; then
  FPR=$(echo \
    | openssl s_client -connect vpn.testdomain.su:443 -servername vpn.testdomain.su 2>/dev/null \
    | openssl x509 -noout -fingerprint -sha256 \
    | cut -d= -f2 | tr -d ':')
else
  FPR=""
fi
echo "OUTLINE_CERT_SHA256=$FPR" >> "$ENV_FILE"

### WireGuard Portal ###
echo -e "\n# WireGuard Portal" >> "$ENV_FILE"
echo "WG_API_URL=http://wg-portal:8888" >> "$ENV_FILE"

# читаем admin token из конфига wg-portal
if [[ -f ./wg-portal/config/config.yaml ]]; then
  WG_TOKEN=$(grep -E '^admin_api_token: ' ./wg-portal/config/config.yaml \
    | head -n1 | awk '{print $2}' | tr -d '"')
else
  WG_TOKEN=""
fi
echo "WG_API_TOKEN=$WG_TOKEN" >> "$ENV_FILE"

echo "✅ Файл $ENV_FILE сгенерирован."
