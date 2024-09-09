from pydantic import BaseModel


class PendingPayload(BaseModel):
    utm_medium: str = "api_test"
    utm_source: str = "api_test"
    utm_campaign: str = "api_test"
    utm_content: str = "api_test"
    utm_term: str = "api_test"
    utm_type: str = "api_test"


class PendingResponse(BaseModel):
    success: bool = True
