from pydantic import BaseModel


class ApplyOfferPayload(BaseModel):
    applicationId: int
    amount: int
    days: int
    tariffId: int
    staffId: int


class ApplyOfferSuccessResponse(BaseModel):
    timestamp: str
    success: bool = True
    response: str = "Предложение успешно сохранено"
