from pydantic import BaseModel


class IssueResponse(BaseModel):
    success: bool = True
