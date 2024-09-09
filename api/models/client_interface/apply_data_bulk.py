from typing import Dict

from pydantic import BaseModel


class BulkStepsPayload(BaseModel):
    passportPageFillDate: str = ""
    personalPageFillDate: str = ""
    jobPageFillDate: str = ""


class BulkField(BaseModel):
    entityId: int
    success: bool
    fieldName: str
    additional: Dict


class ApplyDataBulkResponse(BaseModel):
    addressRegFlat: BulkField
    birthdate: BulkField
    passportIssuerName: BulkField
    jobTitle: BulkField
    bankruptcyProcessed: BulkField
    addressRegHouse: BulkField
    salary: BulkField
    passportIdentifier: BulkField
    addressFactFlat: BulkField
    birthPlace: BulkField
    patronymic: BulkField
    passportIssuerCode: BulkField
    addressFactHouse: BulkField
    jobCompanyName: BulkField
    surname: BulkField
    friendPhone: BulkField
    addressRegId: BulkField
    passportIssueDate: BulkField
    addressFactId: BulkField
    jobType: BulkField
    snils: BulkField
    email: BulkField
    expensesAmount: BulkField


class ApplicationBulkResponse(BaseModel):
    passportPageFillDate: BulkField
    personalPageFillDate: BulkField
    jobPageFillDate: BulkField


class PayToolPayload(BaseModel):
    currentPaytool: int


class Paytool(BaseModel):
    entityId: int
    success: bool
    fieldName: str
    additional: Dict


class PayToolResponse(BaseModel):
    currentPaytool: Paytool
