from typing import Dict

from pydantic import BaseModel


class NewPasswordPayload(BaseModel):
    password: str


class ForgotPasswordResponse(BaseModel):
    success: bool = True
    data: Dict = {}
