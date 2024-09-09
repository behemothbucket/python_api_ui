from pydantic import BaseModel


class AdditionalInfoPayload(BaseModel):
    clientType: str = "REGULAR"
    fingerprint: str = ""


class AdditionalInfoResponse(BaseModel):
    timestamp: str
    success: bool = True
