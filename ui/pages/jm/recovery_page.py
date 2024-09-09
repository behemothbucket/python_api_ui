import allure

from ui.core.locator import Input, Locator
from ui.core.page import Page
from ui.pages.jm.components import AuthForm, Header
from ui.utils.constants.routes import UIRoutes


class RecoveryPage(Page):

    def __init__(self):
        self.Header = Header()
        self.phone_input = AuthForm.phone_input
        self.password_input = AuthForm.otp_code_input
        self.recovery_phone_input = Input(
            "Recovery Phone Input", '//input[@name="phone"]'
        )
        self.recovery_sms_input = Input(
            "Recovery SMS Input", '//input[@name="recoveryCheckSMS"]'
        )
        self.new_password_input = Input(
            "New Password Input", '//input[@name="newPassword"]'
        )
        self.repeat_new_password_input = Input(
            "Repeat New Password Input", '//input[@name="repeatNewPassword"]'
        )
        self.forgot_password_button = Locator(
            "Forgot Password Button", '//a[text()="Я не помню пароль"]'
        )
        self.next_button = Locator("Next Button", '//button[text()="Далее"]')
        self.change_password_button = Locator(
            "Change Password Button", '//button[contains(text(), "Сменить пароль")]'
        )
        self.login_button = Locator("Login Button", '//button[text()="Войти"]')

    @allure.step("Ввод номера телефона восстановления: '{recovery_phone_number}'")
    def fill_phone_number(self, recovery_phone_number: str):
        self.phone_input.press_sequentially(recovery_phone_number)

    @allure.step("Нажать на кнопку 'Я не помню пароль'")
    def click_on_forgot_password_button(self):
        self.forgot_password_button.click()
        self.wait_for_url(UIRoutes.RECOVERY_PAGE_BASE)

    @allure.step("Ввод номера телефона: '{recovery_phone_number}' и SMS '{sms_code}'")
    def fill_recovery_phone_number_and_sms(
        self, recovery_phone_number: str, sms_code: str
    ):
        self.recovery_phone_input.press_sequentially(recovery_phone_number)
        self.next_button.click()
        self.recovery_sms_input.input(sms_code)
        self.next_button.click()

    @allure.step("Ввод нового пароля 2 раза: '{recovery_password}'")
    def fill_new_password(self, recovery_password: str):
        self.new_password_input.input(recovery_password)
        self.repeat_new_password_input.input(recovery_password)

    @allure.step("Нажать на кнопку 'Сменить пароль'")
    def click_change_password_button(self):
        self.change_password_button.click()

    @allure.step("Нажать на кнопку 'Войти'")
    def click_login_button(self):
        self.login_button.click()

    @allure.step("Проверка: Открыта страница авторизации")
    def is_login_page(self):
        self.wait_for_url(UIRoutes.LOGIN_PAGE)

    @allure.step("Проверка: Открыта страница ЛК")
    def is_lk_page(self):
        try:
            self.wait_for_url(UIRoutes.LK_PAGE)
        except TimeoutError:
            self.wait_for_url(UIRoutes.PROFILE_PAGE)

    @allure.step("Ввод пароля: '{password}'")
    def fill_password(self, password: str):
        self.password_input.input(password)

    @allure.step("Нажать на кнопку 'Далее'")
    def click_next_button(self):
        self.next_button.click()
