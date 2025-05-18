import os
import httpx
from pritunl_api import Pritunl
from outline_vpn.outline_vpn import OutlineVPN

# ───────── X-UI (VLESS+Reality) ─────────
XUI_BASE_URL = os.getenv("XUI_BASE_URL", "http://xui:54321")
XUI_USERNAME = os.getenv("XUI_USERNAME", "admin")
XUI_PASSWORD = os.getenv("XUI_PASSWORD", "secret")
XUI_INBOUND_ID = os.getenv("XUI_INBOUND_ID", "")

xui_client = httpx.Client(base_url=XUI_BASE_URL)
_login = xui_client.post("/login", json={
    "username": XUI_USERNAME, "password": XUI_PASSWORD
})
if _login.status_code != 200:
    raise RuntimeError(f"X-UI login failed: {_login.text}")

# ───────── Pritunl (OpenVPN) ─────────
PRITUNL_BASE_URL = os.getenv("PRITUNL_BASE_URL", "")
PRITUNL_API_TOKEN = os.getenv("PRITUNL_API_TOKEN", "")
PRITUNL_API_SECRET = os.getenv("PRITUNL_API_SECRET", "")
PRITUNL_ORG_ID = os.getenv("PRITUNL_ORG_ID", "")

pritunl = Pritunl(
    url=PRITUNL_BASE_URL,
    token=PRITUNL_API_TOKEN,
    secret=PRITUNL_API_SECRET
)

# ───────── Outline (Shadowbox) ─────────
OUTLINE_API_URL = os.getenv("OUTLINE_API_URL")
OUTLINE_CERT_SHA256 = os.getenv("OUTLINE_CERT_SHA256")
outline = OutlineVPN(
    api_url=OUTLINE_API_URL,
    cert_sha256=OUTLINE_CERT_SHA256
)

# ───────── WireGuard Portal ─────────
WG_API_URL = os.getenv("WG_API_URL", "http://wg-portal:8888")
WG_API_TOKEN = os.getenv("WG_API_TOKEN", "")
wg_client = httpx.Client(
    base_url=WG_API_URL,
    headers={"Authorization": f"Bearer {WG_API_TOKEN}"}
)
