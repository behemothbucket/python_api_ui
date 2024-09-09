import allure
import pytest

from settings.base import base_settings
from ui.core.page import Page
from ui.pages.jm.login_page import LoginPage
from ui.pages.jm.recovery_page import RecoveryPage
from ui.pages.jm.registration_page import RegistrationPage
from utils.constants.qa_annotations import Tasks, Suite, TestCase

test_user = base_settings.test_user


@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
@allure.parent_suite("UI")
@allure.suite(Suite.SMOKE)
@allure.link(Tasks.MAIN_TASK)
@pytest.mark.usefixtures("driver")
class TestJoyMoneySmoke(Page):
    """
    Тестовый класс для проверки основных функций JoyMoney.

    Args:
        Page (class): Базовый класс для всех страниц.
    """

    @allure.testcase(TestCase.AUTHORIZATION)
    @allure.tag("ui", "smoke")
    @allure.title("Авторизация")
    def test_authorization(self):
        """
        Тест авторизации пользователя.

        Шаги:
        1. Открыть страницу авторизации.
        2. Ввести номер телефона и пароль.
        3. Нажать кнопку "Далее".
        4. Проверить, что пользователь попал на страницу личного кабинета.
        """
        phone_number = test_user.phone
        otp_code = test_user.otp_code

        page = LoginPage().open()

        page.fill_phone_number(phone_number)
        page.click_get_code_button()
        page.fill_otp_code(otp_code)
        page.is_lk_page()

    @allure.testcase(TestCase.PASSWORD_RECOVERY)
    @allure.tag("ui", "smoke")
    @allure.title("Восстановление пароля")
    @pytest.mark.skip(reason="Устарел")
    def test_password_recovery(self):
        """
        Тест восстановления пароля пользователя.

        Шаги:
        1. Открыть страницу восстановления пароля.
        2. Ввести номер телефона для восстановления.
        3. Нажать кнопку "Забыли пароль".
        4. Ввести номер телефона и смс-код для восстановления.
        5. Ввести новый пароль.
        6. Нажать кнопку "Изменить пароль".
        7. Нажать кнопку "Войти".
        8. Проверить, что пользователь попал на страницу авторизации.
        9. Ввести номер телефона и новый пароль.
        10. Нажать кнопку "Далее".
        11. Проверить, что пользователь попал на страницу личного кабинета.
        """
        recovery_phone_number = test_user.recovery_phone
        otp_code = test_user.otp_code
        new_password = test_user.new_password

        page = RecoveryPage().open()

        page.fill_phone_number(recovery_phone_number)
        page.click_on_forgot_password_button()
        page.fill_recovery_phone_number_and_sms(recovery_phone_number, otp_code)
        page.fill_new_password(new_password)
        page.click_change_password_button()
        page.click_login_button()
        page.is_login_page()
        page.fill_phone_number(recovery_phone_number)
        page.fill_password(new_password)
        page.click_next_button()
        page.is_lk_page()

    @allure.testcase(TestCase.REGISTRATION)
    @allure.tag("ui", "smoke", "pdl")
    @allure.title("Первак PDL")
    def test_create_first_pdl(self):
        """
        Тест создания первого PDL.

        Шаги:
        1. Открыть страницу регистрации.
        2. Выполнить первый шаг регистрации.
        3. Выполнить второй шаг регистрации.
        4. Выполнить третий шаг регистрации.
        5. Одобрить заявку.
        6. Привязать карту.
        7. Подписать договор.
        8. Дождаться выдачи займа.
        9. Проверить, что пользователь попал на страницу личного кабинета.
        """
        page = RegistrationPage().open()

        page.complete_first_step()
        page.complete_second_step()
        page.complete_third_step()
        page.apply_offer()
        page.add_card()
        page.sign_agreement()
        page.wait_for_issue()
        page.is_lk_page()

        # TODO teardown /delete ?
