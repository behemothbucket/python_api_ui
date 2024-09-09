from typing import List, Optional

from pydantic import BaseModel


class Personal(BaseModel):
    name: str
    surname: str
    patronymic: str
    phone: str
    email: str
    birthDate: str
    addrRegId: str
    addrRegHouse: str
    addrRegFlat: str
    addrFactId: str
    addrFactHouse: str
    addrFactFlat: str


class Passport(BaseModel):
    series: str
    number: str
    issuerCode: str
    issueDate: str
    birthPlace: str
    issuerName: str


class Documents(BaseModel):
    snils: str
    passport: Passport


class Job(BaseModel):
    title: str
    type: int
    company: str


class Person(BaseModel):
    personal: Personal
    id: int
    blocked: bool
    documents: Documents
    job: Job
    expensesAmount: float
    bankruptcyProcessed: bool
    friendPhone: str
    type: int
    clientType: str
    sold: bool
    notPresentedFields: List[Optional[str]]


class Application(BaseModel):
    id: int
    requestAmount: float
    approveAmount: Optional[float] = None
    chosenAmount: Optional[float] = None
    requestDays: int
    approveDays: Optional[int] = None
    chosenDays: Optional[int] = None
    status: int
    approvedToRequestCreditHistory: bool
    gracePeriod: int
    createDate: str
    personalPageFillDate: Optional[str] = None
    passportPageFillDate: Optional[str] = None
    jobPageFillDate: Optional[str] = None
    decisionDate: Optional[str] = None
    amountToPay: float
    canCreateNewApplication: bool
    existFilledApplication: bool
    existExpiredApplication: bool
    flags: List[Optional[str]] = None
    fromExternalClient: bool


class Agreement(BaseModel):
    status: int
    id: int
    signDate: str
    loanMoney: float
    loanDays: int
    factLoanDays: int
    canProlongate: bool
    remainingAmount: float
    fullCost: float
    fullCostOrigin: float
    paidAmount: float
    mainDebt: float
    remainingMainDebt: float
    percentDebt: float
    pan: str
    paymentDate: str
    prolongationsCount: int
    nextPaymentAmount: float
    amountInPlan: float
    overdueDebt: float
    overduePercent: float
    percentByOverdueDebt: float
    hasSupplementaryDocument: bool
    duty: float
    dpd: int
    hadOverdue: bool
    inAgencyCollection: bool
    commission: float
    penalty: float
    longLoan: bool


class InfoResponse(BaseModel):
    person: Person
    application: Application
    agreement: Optional[Agreement] = None
    success: bool = True
