import random

import allure

from api.base.api.jd_api import JdApi
from api.utils.clients.http.builder import get_http_client
from settings.base import base_settings
from ui.core.block import Block
from ui.core.driver import Driver
from ui.core.locator import Iframe, Input, Locator
from ui.core.page import Page
from ui.pages.jm.components import AuthForm
from ui.utils.constants.routes import UIRoutes
from utils.constants.js_scripts import Script
from utils.faker.client.fake_client import FakeUser
from utils.faker.client.fake_data import FakeData
from utils.logger import logger

test_user = base_settings.test_user
acquiring = base_settings.acquiring


class RegistrationPage(Page):

    def __init__(self):
        self.fake_user = FakeUser()
        self.phone_input = AuthForm.phone_input
        self.otp_code_input = AuthForm.otp_code_input
        self.auth_documents_main_checkbox = AuthForm.documents_main_checkbox
        self.get_code_button = AuthForm.get_code_button

        self.name_input = Input("Поле Имя", '//input[@name="userName"]')

        self.personal_fields = Block(
            "Шаг 1",
            '//form[@id="PersonalForm"]',
            surname_input=Input("Поле Фамилия", '//input[@name="surname"]'),
            patronymic_input=Input("Поле Отчество", '//input[@name="patronymic"]'),
            birthdate_input=Input("Поле Дата рождения", '//input[@name="birthdate"]'),
            email_input=Input("Поле Email", '//input[@name="email"]'),
        )

        self.first_step_next_button = Locator(
            "Кнопка Далее в [Шаг 1]", '//button[@id="sendPersonalFormBtn"]'
        )

        self.passport_address_fields = Block(
            "Шаг 2",
            '//form[@id="PassportForm"]',
            passport_identifier_input=Input(
                "Поле Серия и номер", '//input[@id="Серия и номер*"]'
            ),
            passport_issue_date_input=Input(
                "Поле Дата выдачи", '//input[@id="Дата выдачи*"]'
            ),
            passport_issuer_code_input=Input(
                "Поле Код подразделения", '//input[@id="Код подразделения*"]'
            ),
            passport_issuer_name_input=Input(
                "Поле Кем выдан", '//input[@id="Кем выдан*"]'
            ),
            birthplace_input=Input(
                "Поле Место рождения", '//input[@id="Место рождения*"]'
            ),
            snils_input=Input("Поле СНИЛС", '//input[@id="СНИЛС*"]'),
            address_reg_city_input=Input(
                "Поле Населенный пункт", '//input[@name="addressRegCity"]'
            ),
            address_reg_street_input=Input(
                "Поле Улица", '//input[@name="addressRegStreet"]'
            ),
            address_reg_house_input=Input(
                "Поле Дом", '//input[@name="addressRegHouse"]'
            ),
            address_reg_flat_input=Input(
                "Поле Квартира", '//input[@name="addressRegFlat"]'
            ),
        )

        self.registered_address_true_checkbox = Locator(
            "Чек-бокс (true) Проживаете по адресу регистрации?",
            '//input[@name="radioAddressFact" and @value="true"]/following-sibling::span[contains(@class,"radioIcon")]',
        )
        self.registered_address_false_checkbox = Locator(
            "Чек-бокс (false) Проживаете по адресу регистрации?",
            '//input[@name="radioAddressFact" and @value="false"]/following-sibling::span[contains(@class,"radioIcon")]',
        )

        self.second_step_next_button = Locator(
            "Кнопка Далее в [Шаг 2]", '//button[@id="sendPassportFormBtn"]'
        )

        self.upload_passport_photos_input = Input(
            "Поле загрузки фото", '//input[@id="uploadPassport"]'
        )
        self.upload_photo_next_button = Locator(
            "Кнопка Далее в форме паспорта", '//span[text()="Далее"]'
        )
        self.upload_photo_label = Locator(
            "(псевдо) Кнопка Далее в форме паспорта", '//label[@for="uploadPassport"]'
        )
        self.job_type_input = Input("Список Тип занятости", '//input[@name="jobType"]')
        self.job_type_li = Locator("Вариант Типа Занятости", '//ul//li[text()=""]')
        self.job_company_name_input = Input(
            "Поле Наименование организации", '//input[@name="jobCompanyName"]'
        )
        self.job_company_title_input = Input(
            "Поле Должность", '//input[@name="jobTitle"]'
        )
        self.salary_input = Input("Поле Доходы", '//input[@name="salary"]')
        self.expenses_input = Input("Поле Расходы", '//input[@name="expensesAmount"]')
        self.bankruptcy_radiobutton = Locator(
            "Чек-бокс Банкротство?",
            '//input[@name="bankruptcyProcessed" and '
            '@value=""]/following-sibling::span[contains(@class,"radioIcon")]',
        )
        self.additional_phone_input = Input(
            "Поле Дополнительный телефон", '//input[@name="friendPhone"]'
        )
        self.application_main_documents_checkbox = Locator(
            "Чек-бокс все документы по заявке",
            '//span[text()="Согласен с подписанием '
            'документов"]/preceding-sibling::label',
        )
        self.send_application_button = Locator(
            "Кнопка Отправить заявку", '//button[text()="Отправить заявку"]'
        )
        self.asp_input = Input(
            "Поле ASP", '(//input[@inputmode="tel" and @type="text"])[]'
        )

        self.new_or_current_loan_button = Locator(
            "Кнопка Действующий займ или Новый займ",
            '//a[text()="Действующий займ" or text()="Новый займ"]',
        )

        self.application_id_div = Locator(
            "Займ №...", '//div[@id="pending_pdl" or @id="approved_pdl"]/span'
        )

        self.add_card_button = Locator("Указать карту", '//button[@id="add_card"]')

        self.add_card_input = Input("Поле Ваша карта*", "//input[@name='paymentTools']")

        self.add_card_li = Locator(
            "Опция Другая карта",
            "//li[@data-value='modal' and text()='Добавить карту']",
        )

        self.payment_iframe = Iframe("Iframe эквайра", "//iframe[@name='payment']")

        self.pan_input = Input("Поле ввода pan в iframe", "//input[@name='pan']")

        self.submit_pan_input = Input(
            "Поле ввода Отправить в iframe",
            "//input[@type='submit']",
        )

        self.close_notice = Locator(
            "Крестик в уведомлении", "//div[@class='notice__close']"
        )

        self.close_frame_span = Locator(
            "Крестик в iframe",
            "//div[@class='portal']//span[contains(@class, 'close')]",
        )

        self.get_money_button = Locator(
            "Кнопка Получить деньги", "//button[@id='get_money']"
        )

        self.ok_thank_you_button = Locator(
            "Кнопка Хорошо, спасибо!", "//button[text()='Хорошо, спасибо!']"
        )

    def _remove_ads(self):
        """
        Удаляет рекламные виджеты со страницы.
        """
        Driver().page.wait_for_timeout(1_000)  # FIXME: Flaky, заменить на другое ивент
        self.evaluate(Script.REMOVE_USEDESK_WIDGET)
        self.evaluate(Script.REMOVE_FLOCKTORY_WIDGET)

    @classmethod
    def _fill_data_fields(cls, values: list[str], block: Block):
        """
        Заполняет поля данными.

        Args:
            values (list[str]): Список значений для заполнения.
            block (Block): Блок с полями для заполнения.
        """
        fields = [
            field for field in block.__dict__.values() if isinstance(field, Input)
        ]
        Block.input_all_blocks(fields, values)

    @allure.step("Шаг 1")
    def complete_first_step(self):
        """
        Выполняет первый шаг регистрации.
        """
        self._fill_phone_number(self.fake_user.phone_number)
        self._fill_otp_code(test_user.otp_code)
        self._click_main_document_checkbox()
        self._click_next_button()
        self._fill_name(self.fake_user.name)
        self._click_next_button()
        self.wait_for_url(UIRoutes.PROFILE_PAGE)
        self._fill_data_fields(
            self.fake_user.values(exclude={"name"}), self.personal_fields
        )
        self._click_first_step_next_button()

    @allure.step("Шаг 2")
    def complete_second_step(self):
        """
        Выполняет второй шаг регистрации.
        """
        self.wait_for_url(UIRoutes.PASSPORT_PAGE)
        self._fill_data_fields(self.fake_user.values(), self.passport_address_fields)
        self._click_registered_address_checkbox()
        self._click_second_step_next_button()
        self._remove_ads()
        self._upload_passport_photos()

    @allure.step("Шаг 3")
    def complete_third_step(self):
        """
        Выполняет третий шаг регистрации.
        """
        self.wait_for_url(UIRoutes.JOB_PAGE)
        self._fill_job_info()
        self._fill_salary_and_expenses(
            self.fake_user.salary, self.fake_user.expensesAmount
        )
        self._click_bankruptcy_checkbox()
        self._fill_additional_phone_number(self.fake_user.friendPhone)
        self._click_all_application_documents_checkbox()
        self._click_send_application_button()
        self._fill_asp(test_user.asp_code)
        self._check_decision_page()

    @allure.step("Одобрение заявки")
    def apply_offer(self):
        """
        Одобряет заявку.
        """
        self._apply_offer()

    @allure.step("Привязка карты карты")
    def add_card(self):
        """
        Привязывает карту.
        """
        self._click_add_card_button()
        self._click_another_card()
        self._send_card_data()

    @allure.step("Подписание договора")
    def sign_agreement(self):
        """
        Подписывает договор.
        """
        self._click_get_money_button()
        self._fill_asp(test_user.asp_code)

    @allure.step("Ввод номера телефона: {phone_number}")
    def _fill_phone_number(self, phone_number: str):
        """
        Вводит номер телефона.

        Args:
            phone_number (str): Номер телефона для ввода.
        """
        self.phone_input.press_sequentially(phone_number)

    @allure.step("Ввод OTP-кода: {code}")
    def _fill_otp_code(self, code: str):
        """
        Вводит смс-код.

        Args:
            code (str): OTP-код для ввода.
        """
        self.otp_code_input.input(code)

    @allure.step("Отметить все ознакомительные документы")
    def _click_main_document_checkbox(self):
        """
        Отмечает все ознакомительные документы.
        """
        self.auth_documents_main_checkbox.click()

    @allure.step("Нажать кнопку 'ПОЛУЧИТЬ КОД'")
    def _click_next_button(self):
        """
        Нажимает кнопку 'ПОЛУЧИТЬ КОД'.
        """
        self.get_code_button.click()

    @allure.step("Ввод имени: {name}")
    def _fill_name(self, name: str):
        """
        Вводит имя.

        Args:
            name (str): Имя для ввода.
        """
        self.name_input.press_sequentially(name)

    @allure.step("Нажать кнопку 'Далее' на первом шаге")
    def _click_first_step_next_button(self):
        """
        Нажимает кнопку 'Далее' на первом шаге.
        """
        self.first_step_next_button.click()
        # Driver().page.wait_for_timeout(1_000)  # Убрать, если перестало зависать

    @allure.step("Нажать на чек-бокс Проживаете по адресу регистрации? (Да)")
    def _click_registered_address_checkbox(self):
        """
        Нажимает на чек-бокс "Проживаете по адресу регистрации?" (Да).
        """
        self.registered_address_true_checkbox.click()

    @allure.step("Нажать кнопку 'Далее' на втором шаге")
    def _click_second_step_next_button(self):
        """
        Нажимает кнопку 'Далее' на втором шаге.
        """
        self.second_step_next_button.click()

    @allure.step("Загрузить фото паспорта")
    def _upload_passport_photos(self):
        """
        Загружает фото паспорта.
        """
        paths = ["resources/img/passport.jpg"] * 3
        self.file_chooser_upload(paths, element=self.upload_passport_photos_input)
        self.upload_photo_next_button.is_visible()
        self.upload_photo_label.click()

    @allure.step("Заполнение данных о месте работы")
    def _fill_job_info(self):
        """
        Заполняет данные о месте работы.
        """
        self.job_type_input.click()

        job_type = FakeData.generate_job_type(return_id=False)

        with allure.step("Выбрать тип занятости"):
            new_xpath = self.job_type_li.xpath.replace('""', f'"{job_type}"')
            self.job_type_li.xpath = new_xpath
            self.job_type_li.click()

            if job_type == "Полная":
                self.job_company_name_input.press_sequentially(
                    self.fake_user.jobCompanyName
                )
                self.job_company_title_input.press_sequentially(self.fake_user.jobTitle)

    @allure.step("Заполнение Доходы ({salary} руб) и расходы ({expenses} руб.)")
    def _fill_salary_and_expenses(self, salary: str, expenses: str):
        """
        Заполняет поля доходов и расходов.

        Args:
            salary (str): Значение дохода.
            expenses (str): Значение расходов.
        """
        self.salary_input.press_sequentially(salary)
        self.expenses_input.press_sequentially(expenses)

    @allure.step("Нажать на чек-бокс банкротство (Нет)")
    def _click_bankruptcy_checkbox(self):
        """
        Нажимает на чек-бокс банкротства (Нет).
        """
        is_bankrupt = random.choice(["true", "false"])
        new_xpath = self.bankruptcy_radiobutton.xpath.replace('""', f'"{is_bankrupt}"')
        self.bankruptcy_radiobutton.xpath = new_xpath
        self.bankruptcy_radiobutton.click()

    @allure.step("Ввести номер дополнительный номер телефона")
    def _fill_additional_phone_number(self, phone_number: str):
        """
        Вводит дополнительный номер телефона.

        Args:
            phone_number (str): Номер телефона для ввода.
        """
        self.additional_phone_input.press_sequentially(phone_number)

    @allure.step("Отметить все документы по заявке")
    def _click_all_application_documents_checkbox(self):
        """
        Отмечает все документы по заявке.
        """
        self.application_main_documents_checkbox.click()

    @allure.step("Нажать на кнопку Отправить заявку")
    def _click_send_application_button(self):
        """
        Нажимает на кнопку "Отправить заявку".
        """
        self.send_application_button.click()

    @allure.step("Ввести ASP {asp}")
    def _fill_asp(self, asp: str):
        """
        Вводит ASP код.

        Args:
            asp (str): ASP код для ввода.
        """
        for i, char in enumerate(asp, start=1):
            xpath = self.asp_input.xpath.replace("[]", f"[{i}]")
            asp_field = Driver().page.locator(xpath)
            asp_field.fill(char)
            logger.info(f"Ввод ASP: {char}")

    @allure.step("Проверка текущей страницы решения по заявке")
    def _check_decision_page(self):
        """
        Проверяет текущую страницу решения по заявке.
        """
        self.wait_for_url(UIRoutes.LK_PAGE)
        self.new_or_current_loan_button.is_visible()

    def _apply_offer(self):
        """
        Одобряет заявку через API.
        """
        logger.info("Одобрение заявки")

        jd_api = JdApi(client=get_http_client(base_url=JdApi.base_url))

        application_id = self.application_id_div.text(get_number=True)
        amount = 10_000
        days = 21
        tariff_id = 45

        jd_api.post_apply_offer(
            application_id=application_id,
            amount=amount,
            days=days,
            tariff_id=tariff_id,
        )

        self.reload()

    @allure.step("Нажать на кнопку Указать карту")
    def _click_add_card_button(self):
        """
        Нажимает на кнопку "Указать карту".
        """
        self.add_card_button.click()

    @allure.step("Нажать Другая карта")
    def _click_another_card(self):
        """
        Нажимает на опцию "Другая карта".
        """
        self.add_card_input.click()
        self.press_key("Enter")
        self.payment_iframe.wait_for_visible()

    @allure.step("Отправить данные карты")
    def _send_card_data(self):
        """
        Отправляет данные карты.
        """
        pan_input = self.payment_iframe.locator(self.pan_input)
        pan_input.clear()
        pan_input.fill(acquiring.alfa_card_pan)

        submit_pan_input = self.payment_iframe.locator(self.submit_pan_input)
        submit_pan_input.click()

        if self.close_notice.is_visible():
            self.close_notice.click()

        if self.close_frame_span.is_visible():
            self.close_frame_span.click()

    @allure.step("Нажать на кнопку Получить деньги")
    def _click_get_money_button(self):
        """
        Нажимает на кнопку "Получить деньги".
        """
        self.get_money_button.click()

    @allure.step("Ожидание выдачи средств")
    def wait_for_issue(self):
        """
        Ожидает выдачи средств.
        """
        if self.ok_thank_you_button.wait_for_visible(timeout=10_000):
            self.ok_thank_you_button.click()

    @allure.step("Проверка: Открыта страница ЛК")
    def is_lk_page(self):
        """
        Проверяет, что открыта страница ЛК.
        """
        self.wait_for_url(UIRoutes.LK_PAGE)
