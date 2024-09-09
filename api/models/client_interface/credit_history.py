from pydantic import BaseModel


class CreditHistoryResponse(BaseModel):
    success: bool = True
