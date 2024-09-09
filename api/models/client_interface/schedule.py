from typing import List

from pydantic import BaseModel


class PaymentData(BaseModel):
    id: int
    date: str
    payment: float
    percent: float
    debt: float
    status: str


class ScheduleResponse(BaseModel):
    root: List[PaymentData]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
