from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.config import outline

router = APIRouter()

class OutlineKey(BaseModel):
    key_id: str
    name: str
    access_url: str
    data_limit: int

@router.get("/keys", response_model=List[OutlineKey])
def list_outline_keys():
    try:
        return outline.get_keys()
    except Exception as e:
        raise HTTPException(502, f"Outline API error: {e}")

@router.post("/keys", response_model=OutlineKey)
def create_outline_key():
    try:
        return outline.create_key()
    except Exception as e:
        raise HTTPException(502, f"Outline API error: {e}")

@router.delete("/keys/{key_id}")
def delete_outline_key(key_id: str):
    try:
        outline.delete_key(key_id)
    except Exception as e:
        raise HTTPException(502, f"Outline API error: {e}")
    return {"detail": "deleted"}
