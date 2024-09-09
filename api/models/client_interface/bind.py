from typing import Dict

from pydantic import BaseModel


class BindNewResponse(BaseModel):
    url: str
    method: str
    requestKey: str
    success: bool
    errorCode: int | None
    message: str | None
    details: Dict | None
    requestParams: Dict
