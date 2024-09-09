from pydantic import BaseModel


class SignAgreementResponse(BaseModel):
    success: bool = True
