# app/schemas.py
from pydantic import BaseModel
from typing import Dict, List

class EntityLinkingRequest(BaseModel):
    text: str

class EntityLinkingResponse(BaseModel):
    mentions: Dict[str, List[dict]]
