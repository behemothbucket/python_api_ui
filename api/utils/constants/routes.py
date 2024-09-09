from enum import Enum


class APIRoutes(str, Enum):
    # client-interface
    AUTHORIZE = "***"
    LOGIN = "***"
    CREATE = "***"
    ADDITIONAL_INFO_APPLY = "***"
    APPLY_DATA_BULK = "***"
    APPLICATION_APPLY_DATA_BULK = "***"
    APPLY_CREDIT_HISTORY_REQUEST = "***"
    APPLY_CREDIT_HISTORY_REQUEST_CHECK = "***"
    BIND_NEW = "***"
    SIGN_AGREEMENT = "***"
    ACTIVE = "***"
    PAY = "***"
    PAY_STATUS = "***"
    SIGN_AGREEMENT_CHECK = "***"
    ISSUE = "***"
    SCHEDULE = "***"
    DOCUMENTS = "***"
    PAYMENT_TOOLS = "***"
    INFO = "***"
    PENDING = "***"
    LOGIN_CHECK = "***"
    FORGOT_PASSWORD = "***"
    FORGOT_PASSWORD_CHECK_FIELD = "***"
    FORGOT_PASSWORD_CHECK_SMS = "***"
    SET_NEW_PASSWORD = "***"

    # emulator
    DELETE = "***"
    PROLONGATION = "***"
    APPROVE = "***"
    SUBMIT_PAYMENT = "***"
    SBER_PAYMENT = "***"
    SBER_CHECK = "***"

    # jd-api
    APPLY_OFFER = "***"

    def __str__(self) -> str:
        return self.value
