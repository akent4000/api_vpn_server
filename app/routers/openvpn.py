from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.config import pritunl, PRITUNL_ORG_ID

router = APIRouter()

class CreatePritunlUser(BaseModel):
    name: str
    email: Optional[str] = None
    disabled: Optional[bool] = False

@router.get("/users")
def list_openvpn_users():
    return pritunl.user.all(org_id=PRITUNL_ORG_ID)

@router.post("/users")
def add_openvpn_user(user: CreatePritunlUser):
    return pritunl.user.create(
        organization_id=PRITUNL_ORG_ID,
        name=user.name,
        email=user.email
    )

@router.delete("/users/{user_id}")
def delete_openvpn_user(user_id: str):
    return pritunl.user.delete(
        organization_id=PRITUNL_ORG_ID,
        user_id=user_id
    )
