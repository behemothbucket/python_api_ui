from typing import Optional
from pydantic import BaseModel
from settings.base import base_settings

test_user = base_settings.test_user


class LoginPayload(BaseModel):
    otpCode: str = test_user.otp_code
    phone: str = test_user.phone
    fingerprint: str = ""


class ExistResponse(BaseModel):
    personType: str = "EXIST"
    personId: int
    appliedApplicationDocuments: bool = True
    success: bool = True


class NewResponse(BaseModel):
    personType: str = "NEW"
    appliedApplicationDocuments: bool = False
    success: bool = True


class LoginExistResponse(BaseModel):
    timestamp: str
    success: bool = True
    response: ExistResponse


class LoginNewResponse(BaseModel):
    timestamp: str
    success: bool = True
    response: NewResponse
