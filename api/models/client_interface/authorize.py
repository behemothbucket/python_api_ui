import time

from pydantic import BaseModel, Field


class Cpa(BaseModel):
    ym_id: str = Field(default=str(int(time.time() * 1000)))


class AuthorizePayload(BaseModel):
    phone: str
    amount: str
    days: str
    cpa: Cpa = Cpa()


class AuthorizeResponse(BaseModel):
    timestamp: str
    success: bool = True
