from pydantic import BaseModel

from api.models.client_interface.apply_data_bulk import BulkField
from api.models.client_interface.info import Person, Application, Agreement
from api.models.client_interface.pay import PaymentPageData
from api.models.client_interface.payment_tools import PaymentTool
from api.models.client_interface.schedule import PaymentData
from api.utils.assertions.base.expect import expect


def assert_authorize(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.timestamp).set_description(
        'Field "timestamp"'
    ).to_be_equal(actual_response["timestamp"])

    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )


def assert_create(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.timestamp).set_description(
        'Field "timestamp"'
    ).to_be_equal(actual_response["timestamp"])

    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )


def assert_additional_info_appy(
    expected_response: BaseModel, actual_response: BaseModel
):
    expect(expected_response.timestamp).set_description(
        'Field "timestamp"'
    ).to_be_equal(actual_response["timestamp"])

    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )


def assert_login(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.timestamp).set_description(
        'Field "timestamp"'
    ).to_be_equal(actual_response["timestamp"])

    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )

    if "personType" in actual_response["response"]:
        expect(expected_response.response.personType).set_description(
            'Field "response.personType"'
        ).to_be_equal(actual_response["response"]["personType"])

    if "personId" in actual_response["response"]:
        expect(expected_response.response.personId).set_description(
            'Field "response.personId"'
        ).to_be_equal(actual_response["response"]["personId"])

    if "appliedApplicationDocuments" in actual_response["response"]:
        expect(expected_response.response.appliedApplicationDocuments).set_description(
            'Field "response.appliedApplicationDocuments"'
        ).to_be_equal(actual_response["response"]["appliedApplicationDocuments"])

    if "success" in actual_response["response"]:
        expect(expected_response.response.success).set_description(
            'Field "response.success"'
        ).to_be_equal(actual_response["response"]["success"])


def assert_check(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.active).set_description('Field "active"').to_be_equal(
        actual_response["active"]
    )

    expect(*expected_response.authorities).set_description(
        'Field "authorities" state'
    ).to_be_equal(*actual_response["authorities"])

    if "personId" in actual_response:
        expect(expected_response.personId).set_description(
            'Field "personId"'
        ).to_be_equal(actual_response["personId"])


def assert_info(expected_response: BaseModel, actual_response: BaseModel):
    person = expected_response.person.model_dump_json()
    application = expected_response.application.model_dump_json()

    if isinstance(person, Person):
        expect(person).set_description('Field "person"').to_be_equal(
            actual_response["person"]
        )

    if isinstance(application, Application):
        expect(application).set_description('Field "application"').to_be_equal(
            actual_response["application"]
        )

    if (
        hasattr(expected_response, "agreement")
        and expected_response.agreement is not None
    ):
        agreement = expected_response.agreement.model_dump_json()
        if "agreement" in actual_response and isinstance(agreement, Agreement):
            expect(agreement).set_description('Field "agreement"').to_be_equal(
                actual_response["agreement"]
            )

    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )


def assert_active(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.status).set_description('Field "status"').to_be_equal(
        actual_response["status"]
    )

    expect(expected_response.id).set_description('Field "id"').to_be_equal(
        actual_response["id"]
    )

    expect(expected_response.signDate).set_description('Field "signDate"').to_be_equal(
        actual_response["signDate"]
    )

    expect(expected_response.loanMoney).set_description(
        'Field "loanMoney"'
    ).to_be_equal(actual_response["loanMoney"])

    expect(expected_response.loanDays).set_description('Field "loanDays"').to_be_equal(
        actual_response["loanDays"]
    )

    expect(expected_response.factLoanDays).set_description(
        'Field "factLoanDays"'
    ).to_be_equal(actual_response["factLoanDays"])

    expect(expected_response.canProlongate).set_description(
        'Field "canProlongate"'
    ).to_be_equal(actual_response["canProlongate"])

    expect(expected_response.fullCost).set_description('Field "fullCost"').to_be_equal(
        actual_response["fullCost"]
    )

    expect(expected_response.fullCostOrigin).set_description(
        'Field "fullCostOrigin"'
    ).to_be_equal(actual_response["fullCostOrigin"])

    expect(expected_response.pan).set_description('Field "pan"').to_be_equal(
        actual_response["pan"]
    )

    expect(expected_response.paymentDate).set_description(
        'Field "paymentDate"'
    ).to_be_equal(actual_response["paymentDate"])

    expect(expected_response.prolongationsCount).set_description(
        'Field "prolongationsCount"'
    ).to_be_equal(actual_response["prolongationsCount"])

    expect(expected_response.hasSupplementaryDocument).set_description(
        'Field "hasSupplementaryDocument"'
    ).to_be_equal(actual_response["hasSupplementaryDocument"])

    expect(expected_response.hadOverdue).set_description(
        'Field "hadOverdue"'
    ).to_be_equal(actual_response["hadOverdue"])

    expect(expected_response.inAgencyCollection).set_description(
        'Field "inAgencyCollection"'
    ).to_be_equal(actual_response["inAgencyCollection"])

    expect(expected_response.longLoan).set_description('Field "longLoan"').to_be_equal(
        actual_response["longLoan"]
    )


def assert_password_recovery(
    expected_response: BaseModel, actual_response: BaseModel | bool
):
    if isinstance(actual_response, bool):
        expect(expected_response.success).set_description(
            "Success true/false"
        ).to_be_equal(actual_response)
        return

    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )

    if "data" in actual_response:
        expect(expected_response.data).set_description('Field "data"').to_be_equal(
            actual_response["data"]
        )


def assert_bulk_fields(expected_response: BaseModel, actual_response: BaseModel):
    for field_name, expected_field in expected_response.__dict__.items():
        if isinstance(expected_field, BulkField):
            expect(actual_response[field_name]["entityId"]).set_description(
                f'Field "{field_name}" - entityId'
            ).to_be_equal(expected_field.entityId)
            expect(actual_response[field_name]["success"]).set_description(
                f'Field "{field_name}" - success'
            ).to_be_equal(expected_field.success)
            expect(actual_response[field_name]["fieldName"]).set_description(
                f'Field "{field_name}" - fieldName'
            ).to_be_equal(expected_field.fieldName)
            expect(actual_response[field_name]["additional"]).set_description(
                f'Field "{field_name}" - additional'
            ).to_be_equal(expected_field.additional)


def assert_documents(actual_response: BaseModel):
    for value in actual_response.values():
        expect(value).set_description('Value is type of "int"').to_be_instance_of(
            value, int
        )


def assert_credit_history(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )


def assert_credit_history_code(expected_response: bool, actual_response: bool):
    expect(expected_response).set_description("Success true/false").to_be_equal(
        actual_response
    )


def assert_pending(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )


def assert_bind_new(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.url).set_description('Field "url"').to_be_equal(
        actual_response["url"]
    )

    expect(expected_response.method).set_description('Field "method"').to_be_equal(
        actual_response["method"]
    )

    expect(expected_response.requestKey).set_description(
        'Field "requestKey"'
    ).to_be_equal(actual_response["requestKey"])

    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )

    expect(expected_response.errorCode).set_description(
        'Field "errorCode"'
    ).to_be_equal(actual_response["errorCode"])

    expect(expected_response.message).set_description('Field "message"').to_be_equal(
        actual_response["message"]
    )

    expect(expected_response.details).set_description('Field "details"').to_be_equal(
        actual_response["details"]
    )

    expect(expected_response.requestParams).set_description(
        'Field "requestParams"'
    ).to_be_equal(actual_response["requestParams"])


def assert_submit_payment(expected_response: str, actual_response: str):
    expect(expected_response).set_description("Result message").to_be_equal(
        actual_response
    )


def assert_payment_tools(expected_response: BaseModel, actual_response: list):
    for expected_payment_tool, actual_payment_tool in zip(
        expected_response, actual_response
    ):
        if isinstance(expected_payment_tool, PaymentTool):
            expect(expected_payment_tool.id).set_description('Field "id"').to_be_equal(
                actual_payment_tool["id"]
            )

            expect(expected_payment_tool.maskedPan).set_description(
                'Field "maskedPan"'
            ).to_be_equal(actual_payment_tool["maskedPan"])

            expect(expected_payment_tool.dateCreate).set_description(
                'Field "dateCreate"'
            ).to_be_equal(actual_payment_tool["dateCreate"])

            expect(expected_payment_tool.commissionByPayment).set_description(
                'Field "commissionByPayment"'
            ).to_be_equal(actual_payment_tool["commissionByPayment"])

            expect(expected_payment_tool.providerName).set_description(
                'Field "providerName"'
            ).to_be_equal(actual_payment_tool["providerName"])

            expect(expected_payment_tool.brandCard).set_description(
                'Field "brandCard"'
            ).to_be_equal(actual_payment_tool["brandCard"])

            expect(expected_payment_tool.provider_id).set_description(
                'Field "provider_id"'
            ).to_be_equal(actual_payment_tool["provider_id"])


def assert_bulk_pay_tool(expected_response: BaseModel, actual_response: BaseModel):
    current_paytool = expected_response.currentPaytool
    actual_paytool = actual_response["currentPaytool"]

    expect(current_paytool.entityId).set_description('Field "entityId"').to_be_equal(
        actual_paytool["entityId"]
    )

    expect(current_paytool.success).set_description('Field "success"').to_be_equal(
        actual_paytool["success"]
    )

    expect(current_paytool.fieldName).set_description('Field "fieldName"').to_be_equal(
        actual_paytool["fieldName"]
    )

    expect(current_paytool.additional).set_description(
        'Field "additional"'
    ).to_be_equal(actual_paytool["additional"])


def assert_sign_agreement(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )


def assert_sign_agreement_check(expected_response: bool, actual_response: bool):
    if isinstance(actual_response, bool):
        expect(expected_response).set_description("Success true/false").to_be_equal(
            actual_response
        )


def assert_issue(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )


def assert_schedule(expected_response: BaseModel, actual_response: BaseModel):
    for expected_payment_data, actual_payment_data in zip(
        expected_response, actual_response
    ):
        if isinstance(expected_payment_data, PaymentData):
            expect(expected_payment_data.id).set_description('Field "id"').to_be_equal(
                actual_payment_data["id"]
            )

            expect(expected_payment_data.date).set_description(
                'Field "date"'
            ).to_be_equal(actual_payment_data["date"])

            expect(expected_payment_data.payment).set_description(
                'Field "payment"'
            ).to_be_equal(actual_payment_data["payment"])

            expect(expected_payment_data.percent).set_description(
                'Field "percent"'
            ).to_be_equal(actual_payment_data["percent"])

            expect(expected_payment_data.debt).set_description(
                'Field "debt"'
            ).to_be_equal(actual_payment_data["debt"])

            expect(expected_payment_data.status).set_description(
                'Field "status"'
            ).to_be_equal(actual_payment_data["status"])


def assert_pay(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.result).set_description('Field "result"').to_be_equal(
        actual_response["result"]
    )

    expect(expected_response.message).set_description('Field "message"').to_be_equal(
        actual_response["message"]
    )

    expect(expected_response.codeResult).set_description(
        'Field "codeResult"'
    ).to_be_equal(actual_response["codeResult"])

    payment_page_data = expected_response.paymentPageData.model_dump_json()

    if isinstance(payment_page_data, PaymentPageData):
        expect(payment_page_data).set_description(
            'Field "payment_page_data"'
        ).to_be_equal(actual_response["paymentPageData"])

    expect(expected_response.needThreeDS).set_description(
        'Field "needThreeDS"'
    ).to_be_equal(actual_response["needThreeDS"])


def assert_status(expected_response: BaseModel, actual_response: BaseModel):
    expect(expected_response.requestId).set_description(
        'Field "requestId"'
    ).to_be_equal(actual_response["requestId"])

    expect(expected_response.status).set_description('Field "status"').to_be_equal(
        actual_response["status"]
    )

    expect(expected_response.success).set_description('Field "success"').to_be_equal(
        actual_response["success"]
    )
