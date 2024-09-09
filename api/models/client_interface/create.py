from typing import Dict
from pydantic import BaseModel


class CreatePayload(BaseModel):
    clientType: str = "REGULAR"
    cpa: Dict = {}
    name: str


class CreateResponse(BaseModel):
    timestamp: str
    success: bool = True
