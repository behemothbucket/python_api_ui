from typing import TypedDict, List

from pydantic import BaseModel


class CheckResponse(TypedDict):
    active: bool
    personId: int
    authorities: List[str]


class ClientRoleResponse(BaseModel):
    active: bool = True
    personId: int
    authorities: List[str] = ["client"]


class AnonymousRoleResponse(BaseModel):
    active: bool = False
    authorities: List[str] = ["ROLE_ANONYMOUS"]


class NoAuthStateResponse(BaseModel):
    active: bool = False
    authorities: List[str] = ["no_auth_state"]
