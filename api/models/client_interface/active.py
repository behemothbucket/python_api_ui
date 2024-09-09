from pydantic import BaseModel


class ActiveResponse(BaseModel):
    status: int
    id: int
    signDate: str
    loanMoney: float
    loanDays: int
    factLoanDays: int
    canProlongate: bool
    fullCost: float
    fullCostOrigin: float
    pan: str
    paymentDate: str
    prolongationsCount: int
    hasSupplementaryDocument: bool
    hadOverdue: bool
    inAgencyCollection: bool
    longLoan: bool
