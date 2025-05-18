from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.config import xui_client, XUI_INBOUND_ID

router = APIRouter()

class XuiUser(BaseModel):
    id: str
    email: Optional[str]
    flow: Optional[str]
    level: Optional[int]
    remark: Optional[str]
    enable: Optional[bool]
    expiryTime: Optional[str]

class CreateXuiUser(BaseModel):
    id: str
    email: Optional[str] = None
    flow: Optional[str] = None
    level: Optional[int] = 0
    remark: Optional[str] = None
    enable: Optional[bool] = True
    expiryTime: Optional[str] = None

@router.get("/users", response_model=List[XuiUser])
def list_vless_users():
    r = xui_client.get(f"/xui/API/inbounds/get/{XUI_INBOUND_ID}")
    if r.status_code != 200:
        raise HTTPException(502, "X-UI API error")
    return r.json().get("clients", [])

@router.post("/users", response_model=dict)
def add_vless_user(user: CreateXuiUser):
    body = {"id": XUI_INBOUND_ID, **user.dict()}
    r = xui_client.post("/xui/API/inbounds/addClient/", json=body)
    if r.status_code != 200:
        raise HTTPException(502, f"X-UI addClient error: {r.text}")
    return r.json()

@router.delete("/users/{client_id}", response_model=dict)
def delete_vless_user(client_id: str):
    r = xui_client.post(f"/xui/API/inbounds/{XUI_INBOUND_ID}/delClient/{client_id}")
    if r.status_code != 200:
        raise HTTPException(502, f"X-UI delClient error: {r.text}")
    return r.json()
