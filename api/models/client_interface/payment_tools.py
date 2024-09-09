from typing import List

from pydantic import BaseModel


class PaymentTool(BaseModel):
    id: int
    maskedPan: str
    dateCreate: str
    commissionByPayment: float
    providerName: str
    brandCard: str
    provider_id: str


class PaymentToolsResponse(BaseModel):
    root: List[PaymentTool]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
