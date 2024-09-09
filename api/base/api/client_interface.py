import time
from http import HTTPStatus
from typing import Type, TypeVar, Union
from venv import logger

import allure
from pydantic import BaseModel

from api.models.client_interface.active import ActiveResponse
from api.models.client_interface.additional_info import (
    AdditionalInfoPayload, AdditionalInfoResponse)
from api.models.client_interface.apply_data_bulk import (
    ApplicationBulkResponse, ApplyDataBulkResponse, BulkStepsPayload,
    PayToolPayload, PayToolResponse)
from api.models.client_interface.authorize import (AuthorizePayload,
                                                   AuthorizeResponse)
from api.models.client_interface.bind import BindNewResponse
from api.models.client_interface.create import CreatePayload, CreateResponse
from api.models.client_interface.credit_history import CreditHistoryResponse
from api.models.client_interface.forgot_password import (
    ForgotPasswordResponse, NewPasswordPayload)
from api.models.client_interface.info import InfoResponse
from api.models.client_interface.issue import IssueResponse
from api.models.client_interface.login import (ExistResponse,
                                               LoginExistResponse,
                                               LoginNewResponse, LoginPayload,
                                               NewResponse)
from api.models.client_interface.pay import PayResponse
from api.models.client_interface.payment_tools import PaymentToolsResponse
from api.models.client_interface.pending import PendingPayload, PendingResponse
from api.models.client_interface.schedule import ScheduleResponse
from api.models.client_interface.sign_agreement import SignAgreementResponse
from api.models.client_interface.status import PayNewStatus
from api.utils.assertions.base.solutions import assert_status_code
from api.utils.assertions.client_interface import (assert_active,
                                                   assert_additional_info_appy,
                                                   assert_authorize,
                                                   assert_bind_new,
                                                   assert_bulk_fields,
                                                   assert_bulk_pay_tool,
                                                   assert_check, assert_create,
                                                   assert_credit_history,
                                                   assert_credit_history_code,
                                                   assert_documents,
                                                   assert_info, assert_issue,
                                                   assert_login,
                                                   assert_password_recovery,
                                                   assert_pay,
                                                   assert_payment_tools,
                                                   assert_pending,
                                                   assert_schedule,
                                                   assert_sign_agreement,
                                                   assert_sign_agreement_check,
                                                   assert_status)
from api.utils.assertions.schema import validate_schema
from api.utils.clients.http.client import APIClient
from api.utils.constants.routes import APIRoutes
from settings.base import base_settings
from utils.faker.client.fake_client import FakeUser
from utils.logger import log_response

T = TypeVar("T", bound=BaseModel)


class ClientInterface(APIClient):
    """
    Класс для взаимодействия с клиентским интерфейсом API.
    """

    base_url = base_settings.api.base_url_client_interface
    test_user = base_settings.test_user
    person_id = None
    person_check_id = None
    application_id = None
    bind_request_id = None
    pay_request_key = None
    pay_tool_id = int | None
    regular_pay_amount = None
    last_pay_status = None

    @allure.step("POST ***")
    def post_authorize(self, **kwargs) -> "ClientInterface":
        """
        Отправить POST-запрос на авторизацию.

        Args:
            **kwargs: Дополнительные параметры для запроса.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        phone = kwargs.get("phone")
        amount = kwargs.get("amount")
        days = kwargs.get("days")

        payload = AuthorizePayload(phone=phone, amount=amount, days=days)

        response = self.client.post(APIRoutes.AUTHORIZE, json=payload.model_dump())
        url = response.url
        data = response.json()

        log_response("POST", url, payload, data)

        timestamp = data.get("timestamp")

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_authorize(AuthorizeResponse(timestamp=timestamp), data)

        validate_schema(data, AuthorizeResponse.model_json_schema())

        return self

    @allure.step("POST ***")
    def post_login(self, otp_code: str, phone: str) -> "ClientInterface":
        """
        Отправить POST-запрос на вход в систему.

        Args:
            otp_code (str): Пароль для входа.
            phone (str): Номер телефона пользователя.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        payload = LoginPayload(password=otp_code, phone=phone)

        response = self.client.post(APIRoutes.LOGIN, json=payload.model_dump())
        url = response.url
        data = response.json()

        log_response("POST", url, payload, data)

        assert_status_code(response.status_code, HTTPStatus.OK)

        timestamp = data.get("timestamp")
        person_id = data.get("response", {}).get("personId")

        if person_id is not None:
            expected_response = LoginExistResponse(
                timestamp=timestamp, response=ExistResponse(personId=person_id)
            )
        else:
            expected_response = LoginNewResponse(
                timestamp=timestamp, response=NewResponse()
            )

        assert_login(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())
        return self

    @allure.step("POST  ***")
    def post_create(self, name: str) -> "ClientInterface":
        """
        Отправить POST-запрос на создание нового пользователя.

        Args:
            name (str): Имя нового пользователя.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        payload = CreatePayload(name=name)

        response = self.client.post(APIRoutes.CREATE, json=payload.model_dump())
        url = response.url
        data = response.json()

        log_response("POST", url, payload, data)

        timestamp = data.get("timestamp")

        assert_status_code(response.status_code, HTTPStatus.OK)

        expected_response = CreateResponse(timestamp=timestamp)
        assert_create(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("POST ***")
    def post_additional_info_apply(self) -> "ClientInterface":
        payload = AdditionalInfoPayload()

        response = self.client.post(
            APIRoutes.ADDITIONAL_INFO_APPLY, json=payload.model_dump()
        )
        url = response.url
        data = response.json()

        log_response("POST", url, payload, data)

        timestamp = data.get("timestamp")

        assert_status_code(response.status_code, HTTPStatus.OK)

        expected_response = AdditionalInfoResponse(timestamp=timestamp)

        assert_additional_info_appy(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("GET  ***")
    def get_check(self, expected_response: Union[Type[T], T]) -> "ClientInterface":
        """
        Отправить GET-запрос на проверку статуса входа.

        Args:
            expected_response (Union[Type[T], T]): Ожидаемый ответ.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        response = self.client.get(APIRoutes.LOGIN_CHECK)
        url = response.url
        data = response.json()

        log_response("GET", url, response=data)

        assert_status_code(response.status_code, HTTPStatus.OK)

        person_id = data.get("personId")

        expected_response = (
            expected_response(personId=person_id) if person_id else expected_response()
        )

        assert_check(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("GET  ***")
    def get_info(self, expected_status: int) -> "ClientInterface":
        """
        Отправить GET-запрос на получение информации о пользователе.

        Args:
            expected_status (int): Ожидаемый статус заявки.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        response = self.client.get(APIRoutes.INFO)
        url = response.url
        data = response.json()

        log_response("GET", url, response=data)

        person = data.get("person")
        application = data.get("application")
        agreement = data.get("agreement", None)

        self.application_id = application.get("id")

        if expected_status == 8:
            current_status = data["application"]["status"]
            assert (
                current_status == expected_status
            ), f"Заявка не одобрена, текущие статус {current_status} != 8"

        expected_response = InfoResponse(
            person=person, application=application, agreement=agreement
        )

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_info(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("GET ***")
    def get_active(self, expected_status: int) -> "ClientInterface":
        """
        Отправить GET-запрос на получение активного договора.

        Args:
            expected_status (int): Ожидаемый статус договора.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        response = self.client.get(APIRoutes.ACTIVE)
        url = response.url
        data = response.json()

        log_response("GET", url, response=data)

        if expected_status == 16:
            current_status = data["status"]
            assert (
                current_status == expected_status
            ), f"Договор не в 16 статусе, текущий статус {current_status} != 16"

        expected_response = ActiveResponse(**data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_active(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("POST ***")
    def post_apply_data_bulk(self, fake_data: FakeUser) -> "ClientInterface":
        """
        Отправить POST-запрос на массовое применение данных.

        Args:
            fake_data (FakeUser): Поддельные данные пользователя.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        payload = fake_data.model_dump_api()

        response = self.client.post(APIRoutes.APPLY_DATA_BULK, json=payload)
        url = response.url
        data = response.json()

        log_response("POST", url, payload, data)

        expected_response = ApplyDataBulkResponse(**data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_bulk_fields(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("POST  ***")
    def post_documents(self, path: str) -> "ClientInterface":
        """
        Отправить POST-запрос на загрузку документов.

        Args:
            path (str): Путь к файлу документа.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        file_obj = open(path, "rb")
        files = [("files", file_obj), ("files", file_obj), ("files", file_obj)]

        response = self.client.post(APIRoutes.DOCUMENTS, files=files)

        url = response.url
        data = response.json()

        log_response("POST", url, response=data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_documents(data)

        file_obj.close()
        return self

    @allure.step("POST ***")
    def post_bulk_steps(self) -> "ClientInterface":
        """
        Отправить POST-запрос на массовое применение шагов.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        payload = BulkStepsPayload()
        path = APIRoutes.APPLICATION_APPLY_DATA_BULK.format(
            application_id=self.application_id
        )

        response = self.client.post(path, json=payload.model_dump())

        url = response.url
        data = response.json()

        log_response("POST", url, payload, data)

        expected_response = ApplicationBulkResponse(**data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_bulk_fields(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("POST ***")
    def post_apply_credit_history(self) -> "ClientInterface":
        """
        Отправить POST-запрос на применение кредитной истории.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        response = self.client.post(APIRoutes.APPLY_CREDIT_HISTORY_REQUEST)

        url = response.url
        data = response.json()

        log_response("POST", url, response=data)

        expected_response = CreditHistoryResponse()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_credit_history(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("POST ***")
    def post_apply_credit_history_code(self, code: str) -> "ClientInterface":
        """
        Отправить POST-запрос на проверку кода кредитной истории.

        Args:
            code (str): Код для проверки.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        params = {"code": code}

        response = self.client.post(
            APIRoutes.APPLY_CREDIT_HISTORY_REQUEST_CHECK, params=params
        )

        url = response.url
        data = response.json()

        log_response("POST", url, response=data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_credit_history_code(True, data)

        return self

    @allure.step("POST ***")
    def post_issue(self) -> "ClientInterface":
        """
        Отправить POST-запрос на выдачу заявки.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        response = self.client.post(APIRoutes.ISSUE)

        url = response.url
        data = response.json()

        log_response("POST", url, response=data)

        expected_response = IssueResponse()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_issue(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        time.sleep(3)  # Дождаться выдачи

        return self

    def _post_forgot_password(self, path: str, **kwargs) -> "ClientInterface":
        """
        Вспомогательный метод для отправки POST-запроса на восстановление пароля.

        Args:
            path (str): Путь для запроса.
            **kwargs: Дополнительные параметры для запроса.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        params = kwargs
        response = self.client.post(path, params=params)
        url = response.url
        data = response.json()

        log_response("POST", url, response=data)

        expected_response = ForgotPasswordResponse()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_password_recovery(expected_response, data)

        if path != APIRoutes.FORGOT_PASSWORD_CHECK_SMS:
            validate_schema(data, expected_response.model_json_schema())

        return self

    def pending(self) -> "ClientInterface":
        """
        Отправить POST-запрос на ожидание обработки заявки.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        payload = PendingPayload()

        response = self.client.post(APIRoutes.PENDING, json=payload.model_dump())
        url = response.url
        data = response.json()

        log_response("POST", url, payload, data)

        expected_response = PendingResponse()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_pending(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        time.sleep(5)  # СПР

        return self

    @allure.step("POST ***")
    def post_bind_new(self) -> "ClientInterface":
        """
        Отправить POST-запрос на привязку нового платежного инструмента.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        params = {
            "applicationId": self.application_id,
        }

        response = self.client.post(APIRoutes.BIND_NEW, params=params)

        url = response.url
        data = response.json()

        log_response("POST", url, response=data)

        self.bind_request_id = data.get("requestKey")

        expected_response = BindNewResponse(**data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_bind_new(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("POST  ***")
    def get_payment_tools(self):
        """
        Отправить GET-запрос на получение платежных инструментов.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        params = {"forPayment": "true"}

        response = self.client.get(APIRoutes.PAYMENT_TOOLS, params=params)
        url = response.url
        data = response.json()

        log_response("GET", url, params, data)

        self.pay_tool_id = data[0]["id"]  # В данном случае приходит только 1 карта

        expected_response = PaymentToolsResponse(root=data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_payment_tools(expected_response, data)

        return self

    @allure.step("POST ***")
    def post_bulk_payment_tool(self) -> "ClientInterface":
        """
        Отправить POST-запрос на массовое применение платежного инструмента.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        payload = PayToolPayload(currentPaytool=self.pay_tool_id)
        path = APIRoutes.APPLICATION_APPLY_DATA_BULK.format(
            application_id=self.application_id
        )

        response = self.client.post(path, json=payload.model_dump())

        url = response.url
        data = response.json()

        log_response("POST", url, payload, data)

        expected_response = PayToolResponse(**data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_bulk_pay_tool(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("POST ***")
    def post_sign_agreement(self) -> "ClientInterface":
        """
        Отправить POST-запрос на подписание договора.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        response = self.client.post(APIRoutes.SIGN_AGREEMENT)

        url = response.url
        data = response.json()

        log_response("POST", url, response=data)

        expected_response = SignAgreementResponse()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_sign_agreement(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("POST ***")
    def post_sign_agreement_check(self, code: str) -> "ClientInterface":
        """
        Отправить POST-запрос на проверку кода подписания договора.

        Args:
            code (str): Код для проверки.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        params = {"code": code}

        response = self.client.post(APIRoutes.SIGN_AGREEMENT_CHECK, params=params)

        url = response.url
        data = response.json()

        log_response("POST", url, response=data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_sign_agreement_check(True, data)

        return self

    @allure.step("GET ***")
    def get_schedule(
        self, payment_in_plan: int = 0, pay_status: str | None = None
    ) -> "ClientInterface":
        """
        Отправить GET-запрос на получение графика платежей.

        Args:
            payment_in_plan (int): Индекс платежа в плане.
            pay_status (str | None): Ожидаемый статус платежа.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        response = self.client.get(APIRoutes.SCHEDULE)

        url = response.url
        data = response.json()

        log_response("GET", url, response=data)

        self.regular_pay_amount = data[payment_in_plan]["payment"]
        current_pay_status = data[payment_in_plan]["status"]

        if pay_status:
            assert (
                current_pay_status == pay_status
            ), f'Частичный платеж не произведен, текущий статус {current_pay_status} != "DONE"'

        expected_response = ScheduleResponse(root=data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_schedule(expected_response, data)

        return self

    @allure.step("POST ***")
    def post_pay(self, **kwargs) -> "ClientInterface":
        """
        Отправить POST-запрос на оплату.

        Args:
            **kwargs: Дополнительные параметры для запроса.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        amount = kwargs.get("amount", self.regular_pay_amount)
        pay_tool_id = kwargs.get("payToolId", self.pay_tool_id)

        params = {
            "amount": amount,
            "paytoolId": pay_tool_id,
        }

        response = self.client.post(APIRoutes.PAY, params=params)

        url = response.url
        data = response.json()

        log_response("POST", url, params, data)

        self.pay_request_key = data["paymentPageData"]["requestKey"]

        expected_response = PayResponse(paymentPageData=data["paymentPageData"])

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_pay(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("GET ***")
    def get_status(self) -> "ClientInterface":
        """
        Отправить GET-запрос на получение статуса платежа.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        params = {
            "requestId": self.pay_request_key,
        }

        response = self.client.get(APIRoutes.PAY_STATUS, params=params)

        url = response.url
        data = response.json()

        log_response("GET", url, params, data)

        expected_response = PayNewStatus(requestId=self.pay_request_key)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_status(expected_response, data)

        validate_schema(data, expected_response.model_json_schema())

        return self

    @allure.step("POST  ***")
    def post_forgot_password_contact(
        self, contact: str, recovery_type: str = "phone"
    ) -> "ClientInterface":
        """
        Отправить POST-запрос на восстановление пароля по контакту.

        Args:
            contact (str): Контакт для восстановления.
            recovery_type (str): Тип восстановления (по умолчанию "phone").

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        return self._post_forgot_password(
            APIRoutes.FORGOT_PASSWORD, contact=contact, recoveryType=recovery_type
        )

    @allure.step("POST  ***")
    def post_forgot_password_check_field(
        self, phone: str, field_value: str = "undefined"
    ) -> "ClientInterface":
        """
        Отправить POST-запрос на проверку поля восстановления пароля.

        Args:
            phone (str): Телефон для проверки.
            field_value (str): Значение поля для проверки (по умолчанию "undefined").

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        return self._post_forgot_password(
            APIRoutes.FORGOT_PASSWORD_CHECK_FIELD, fieldValue=field_value, phone=phone
        )

    @allure.step("POST  ***")
    def post_forgot_password_check_sms(
        self, code: str, phone: str
    ) -> "ClientInterface":
        """
        Отправить POST-запрос на проверку SMS-кода восстановления пароля.

        Args:
            code (str): Код для проверки.
            phone (str): Телефон для проверки.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        return self._post_forgot_password(
            APIRoutes.FORGOT_PASSWORD_CHECK_SMS, code=code, phone=phone
        )

    @allure.step("POST  ***")
    def post_set_new_password(self, password: str) -> "ClientInterface":
        """
        Отправить POST-запрос на установку нового пароля.

        Args:
            password (str): Новый пароль.

        Returns:
            ClientInterface: Обновленный объект ClientInterface.
        """
        payload = NewPasswordPayload(password=password)

        response = self.client.post(
            APIRoutes.SET_NEW_PASSWORD, json=payload.model_dump()
        )
        url = response.url
        data = response.json()

        log_response("POST", url, payload, data)

        expected_response = ForgotPasswordResponse()

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_password_recovery(expected_response, data)

        validate_schema(data, ForgotPasswordResponse.model_json_schema())

        return self
