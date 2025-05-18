from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.config import wg_client

router = APIRouter()

class WireguardPeer(BaseModel):
    class Config:
        extra = "allow"

class CreateWireguardPeer(BaseModel):
    email: str
    name: str
    publicKey: Optional[str] = None
    presharedKey: Optional[str] = None
    allowedIps: Optional[List[str]] = None

@router.get("/peers/{email}", response_model=List[WireguardPeer])
def list_wireguard_peers(email: str):
    r = wg_client.get(f"/provisioning/peers/{email}")
    if r.status_code != 200:
        raise HTTPException(502, f"WG Portal list error: {r.text}")
    return r.json()

@router.post("/peers", response_model=WireguardPeer)
def add_wireguard_peer(peer: CreateWireguardPeer):
    r = wg_client.post("/provisioning/peers", json=peer.dict())
    if r.status_code not in (200, 201):
        raise HTTPException(502, f"WG Portal create error: {r.text}")
    return r.json()

@router.delete("/peers/{pkey}")
def delete_wireguard_peer(pkey: str):
    r = wg_client.delete(f"/provisioning/peers/{pkey}")
    if r.status_code not in (200, 204):
        raise HTTPException(502, f"WG Portal delete error: {r.text}")
    return {"detail": "deleted"}
