import allure
import pytest

from api.models.client_interface.check import AnonymousRoleResponse, ClientRoleResponse
from settings.base import base_settings
from utils.constants.qa_annotations import Suite, Tasks, TestCase
from utils.constants.tariff import Tariff
from utils.faker.client.fake_client import FakeUser
from utils.logger import log_run_output


@pytest.mark.api
@pytest.mark.client_interface
@allure.feature("client-interface")
@allure.story("client-interface")
@allure.severity(allure.severity_level.CRITICAL)
@allure.parent_suite(Suite.SMOKE)
@allure.suite(Suite.API)
@allure.tag("api", "smoke")
@allure.link(Tasks.MAIN_TASK)
class TestClientInterface:
    """
    Тесты для интерфейса клиента.

    Этот класс содержит тесты для различных операций интерфейса клиента, включая авторизацию,
    восстановление пароля, регистрацию и регулярные платежи.
    """

    @allure.title("Авторизация")
    @allure.testcase(TestCase.AUTHORIZATION)
    def test_authorization(self, api_clients):
        """
        Тест для проверки процесса авторизации.

        Этот тест выполняет следующие шаги:
        1. Получает информацию о клиенте.
        2. Отправляет запрос на авторизацию.
        3. Выполняет вход в систему и проверяет ответ.

        Args:
            api_clients: Объект, содержащий интерфейс клиента и другие необходимые компоненты.
        """
        client_interface, _, _ = api_clients

        test_user = base_settings.test_user

        phone = test_user.phone
        amount = Tariff.generate_random_amount("MEGA_START")
        days = Tariff.generate_random_days("MEGA_START")
        otp_code = test_user.otp_code

        client_interface.get_check(
            expected_response=AnonymousRoleResponse
        ).post_authorize(phone=phone, amount=amount, days=days).post_login(
            otp_code=otp_code, phone=phone
        ).get_check(
            expected_response=ClientRoleResponse
        )

    @allure.testcase(TestCase.PASSWORD_RECOVERY)
    @allure.title("Восстановление пароля")
    @pytest.mark.skip(reason="Устарел")
    def test_password_recovery(self, api_clients):
        """
        Тест для проверки процесса восстановления пароля.

        Этот тест выполняет следующие шаги:
        1. Отправляет запрос на восстановление пароля.
        2. Проверяет SMS-код.
        3. Устанавливает новый пароль и выполняет авторизацию.

        Args:
            api_clients: Объект, содержащий интерфейс клиента и другие необходимые компоненты.
        """
        client_interface, _, _ = api_clients

        test_user = base_settings.test_user

        phone = test_user.recovery_phone
        asp = test_user.asp_code
        password = test_user.new_password
        amount = Tariff.generate_random_amount("MEGA_START")
        days = Tariff.generate_random_days("MEGA_START")

        client_interface.post_forgot_password_contact(
            contact=phone
        ).post_forgot_password_check_field(phone=phone).post_forgot_password_check_sms(
            code=asp, phone=phone
        ).post_set_new_password(
            password=password
        ).post_authorize(
            phone=phone, amount=amount, days=days
        ).post_login(
            password=password
        ).get_check(
            expected_response=ClientRoleResponse
        )

    @allure.step(TestCase.REGISTRATION)
    @allure.title("Регистрация (PDL)")
    def test_registration(self, api_clients):
        """
        Тест для проверки процесса регистрации.

        Этот тест выполняет следующие шаги:
        1. Отправляет запрос на авторизацию.
        2. Выполняет вход в систему.
        3. Создает нового пользователя и отправляет необходимые данные.

        Args:
            api_clients: Объект, содержащий интерфейс клиента и другие необходимые компоненты.
        """
        client_interface, jd_api, _ = api_clients

        fake_user = FakeUser()
        test_user = base_settings.test_user

        phone = fake_user.phone_number
        otp_code = test_user.otp_code
        amount = Tariff.generate_random_amount("MEGA_START")
        days = Tariff.generate_random_days("MEGA_START")
        name = fake_user.name
        path = "resources/img/passport.jpg"
        code = test_user.asp_code

        application_id = (
            client_interface.post_authorize(phone=phone, amount=amount, days=days)
            .post_login(otp_code=otp_code, phone=phone)
            .post_create(name=name)
            .post_additional_info_apply()
            .post_apply_data_bulk(fake_user)
            .post_documents(path=path)
            .get_info(expected_status=5)
            .post_bulk_steps()
            .post_apply_credit_history()
            .post_apply_credit_history_code(code=code)
            .pending()
            .application_id
        )

        jd_api.post_apply_offer(
            application_id=application_id,
            amount=amount,
            days=days,
            tariff_id=Tariff.FIRST_PDL,
        )

        log_run_output(["Номер телефона"], [[phone]])

    @allure.step(TestCase.EARLY_PAYMENT_IL)
    @allure.title("Очередной платеж (IL)")
    def test_pdl_regular_payment(self, api_clients):
        """
        Тест для проверки процесса регулярного платежа.

        Этот тест выполняет следующие шаги:
        1. Отправляет запрос на авторизацию.
        2. Выполняет вход в систему.
        3. Создает нового пользователя и отправляет необходимые данные.
        4. Обрабатывает платеж и проверяет статус.

        Args:
            api_clients: Объект, содержащий интерфейс клиента и другие необходимые компоненты.
        """
        client_interface, jd_api, emulator = api_clients

        fake_user = FakeUser()
        test_user = base_settings.test_user
        acquiring = base_settings.acquiring

        phone = fake_user.phone_number
        password = test_user.otp_code
        amount = Tariff.generate_random_amount("FIRST_IL")
        days = Tariff.generate_random_days("FIRST_IL")
        name = fake_user.name
        path = "resources/img/passport.jpg"
        code = test_user.asp_code
        pan = acquiring.alfa_card_pan

        registration_data = (
            client_interface.post_authorize(phone=phone, amount=amount, days=days)
            .post_login(password=password)
            .post_create(name=name)
            .post_apply_data_bulk(fake_user)
            .post_documents(path=path)
            .post_bulk_steps()
            .post_apply_credit_history()
            .post_apply_credit_history_code(code=code)
            .pending()
        )

        application_id = registration_data.application_id

        jd_api.post_apply_offer(
            application_id=application_id,
            amount=amount,
            days=days,
            tariff_id=Tariff.FIRST_IL.get("id", 165),
        )

        bind_request_id = client_interface.post_bind_new().bind_request_id
        emulator.post_submit_payment(pan=pan, request_id=bind_request_id)

        pay_data = (
            client_interface.get_payment_tools()
            .post_bulk_payment_tool()
            .post_sign_agreement()
            .post_sign_agreement_check(code=code)
            .post_issue()
            .get_info(expected_status=8)
            .get_active(expected_status=16)
            .get_schedule()
            .post_pay()
            .get_status()
        )

        pay_request_id = pay_data.pay_request_key
        emulator.post_submit_payment(pan=pan, request_id=pay_request_id)

        client_interface.get_schedule(pay_status="DONE")

        log_run_output(["Номер телефона"], [[phone]])
