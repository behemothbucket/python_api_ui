import allure

from ui.core.page import Page
from ui.pages.jm.components import AuthForm, LoginHeader
from ui.utils.constants.routes import UIRoutes


class LoginPage(Page):
    """
    Класс для страницы авторизации.

    Атрибуты:
        header (LoginHeader): Заголовок страницы авторизации.
        phone_input (Input): Поле ввода номера телефона.
        password_input (Input): Поле ввода пароля.
        next_button (Button): Кнопка "Далее".
        tid_button (Button): Кнопка TID.
    """

    def __init__(self):
        self.header = LoginHeader()
        self.phone_input = AuthForm.phone_input
        self.get_code_button = AuthForm.get_code_button
        self.password_input = AuthForm.otp_code_input
        self.tid_button = AuthForm.tid_button

    @allure.step("Ввод номера телефона: '{phone_number}'")
    def fill_phone_number(self, phone_number: str):
        """
        Ввод номера телефона в соответствующее поле.

        Аргументы:
            phone_number (str): Номер телефона для ввода.
        """
        self.phone_input.press_sequentially(phone_number)

    @allure.step("Нажать на кнопку ПОЛУЧИТЬ КОД")
    def click_get_code_button(self):
        """
        Нажимает на кнопку "ПОЛУЧИТЬ КОД".

        Этот метод выполняет клик на кнопку, предназначенную для получения кода
        подтверждения, который будет отправлен на указанный номер телефона.

        Исключения:
            Если кнопка не доступна для нажатия, может быть вызвано исключение.
        """
        self.get_code_button.click()

    @allure.step("Ввод OTP-кода: '{code}'")
    def fill_otp_code(self, code: str):
        """
        Ввод OTP-кода в соответствующее поле.

        Аргументы:
            code (str): OTP-код для ввода.
        """
        self.password_input.input(code)

    @allure.step("Проверка: Открыта страница ЛК")
    def is_lk_page(self):
        """
        Проверка, что открыта страница личного кабинета (ЛК).

        Исключения:
            TimeoutError: Если страница ЛК не открыта, проверяет, открыта ли страница профиля.
        """
        try:
            self.wait_for_url(UIRoutes.LK_PAGE)
        except TimeoutError:
            self.wait_for_url(UIRoutes.PROFILE_PAGE)
