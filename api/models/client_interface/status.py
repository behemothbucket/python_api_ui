from pydantic import BaseModel


class PayNewStatus(BaseModel):
    requestId: str
    status: str = "NEW"
    success: bool = True
