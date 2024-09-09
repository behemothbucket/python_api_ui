from ui.core.locator import Input, Locator


class AuthForm:
    phone_input = Input("Поле Номер телефона", '//input[@name="phone"]')
    otp_code_input = Input("Поле OTP", '//input[@type="password"]')
    get_code_button = Locator("Кнопка ПОЛУЧИТЬ КОД", "//button[text()='Получить код']")
    documents_main_checkbox = Locator(
        "Главный чек-бокс документов",
        '//span[text()="Ознакомлен с документами"]/parent::span/preceding-sibling::label',
    )
    tid_button = Locator(
        "T-ID Button", '//div[@id="oauth-buttons"]//button[contains(@class, "tid")]'
    )


class Header:
    logo = Locator("Лого", '//header//a[contains(@class, "logo")]')


class LoginHeader(Header):
    phone = Locator("Телефон горячей линии", '//header//a[contains(@class, "phone")]')


class LkHeader(Header):
    client_name = Locator("Инициалы клиента", '//header//div[contains(@class, "name")]')
    logout_button = Locator(
        "Кнопка Выйти", '//header//button[contains(@class, "logout")]'
    )
