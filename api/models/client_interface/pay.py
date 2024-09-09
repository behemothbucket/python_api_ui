from pydantic import BaseModel


class RequestParams(BaseModel):
    clientIp: str
    PaReq: str
    prolongation: str
    backRef: str
    paytoolId: str
    requestId: str
    amount: str
    agreeId: str


class PaymentPageData(BaseModel):
    url: str
    method: str
    requestKey: str
    success: bool
    errorCode: int | None
    message: str | None
    details: str | None
    requestParams: RequestParams


class PayResponse(BaseModel):
    result: str = "success"
    message: str | None = None
    codeResult: int | None = None
    paymentPageData: PaymentPageData
    needThreeDS: bool = True
