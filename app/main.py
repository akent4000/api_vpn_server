from fastapi import FastAPI
from app.routers import vless, openvpn, outline, wireguard

app = FastAPI(title="VPN API Gateway")

app.include_router(vless.router, prefix="/v1/vless", tags=["vless"])
app.include_router(openvpn.router, prefix="/v1/openvpn", tags=["openvpn"])
app.include_router(outline.router, prefix="/v1/outline", tags=["outline"])
app.include_router(wireguard.router, prefix="/v1/wireguard", tags=["wireguard"])
