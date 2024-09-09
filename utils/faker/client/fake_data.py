from random import random, randint, choice
from string import digits, ascii_letters

from mimesis import Person, Address, Gender, Locale, Finance, Numeric
from mimesis.builtins import RussiaSpecProvider
from mimesis.random import random, Random

from settings.base import base_settings
from utils.faker.dates import FakeDates

test_user = base_settings.test_user
acquiring = base_settings.acquiring


def random_string(start: int = 9, end: int = 15) -> str:
    return "".join(choice(ascii_letters + digits) for _ in range(randint(start, end)))


class FakeData:
    def __init__(self):
        self.person = Person(locale=Locale.RU)
        self.gender = random.choice([Gender.FEMALE, Gender.MALE])
        self.ru = RussiaSpecProvider()
        self.address = Address(locale=Locale.RU)
        self.fin = Finance(locale=Locale.RU)
        self.numeric = Numeric()
        self.random = Random()

    def generate_random_phone_number(self) -> str:
        verification_type = acquiring.approve_emulation

        last_number = {
            "APPROVE": 0,
            "REJECT": 9,
            "VERIFICATION": 5
        }.get(verification_type)

        if last_number is None:
            raise ValueError(
                f"Неверный тип верификации: {verification_type}. Допустимые значения: {last_number.__dict__.keys()}"
            )

        emulator_mask = f"79########{last_number}"
        return self.person.telephone(mask=emulator_mask)

    def generate_russian_name(self) -> str:
        return self.person.first_name(gender=self.gender)

    def generate_russian_surname(self) -> str:
        return self.person.last_name(gender=self.gender)

    def generate_russian_patronymic(self) -> str:
        return self.ru.patronymic(gender=self.gender)

    @classmethod
    def generate_birthdate(cls) -> str:
        return FakeDates.get_random_birthdate()

    def generate_email(self) -> str:
        return self.person.email()

    def generate_passport_issuer_identifier(self) -> str:
        return self.ru.series_and_number().replace(" ", "", 1)

    # FIXME
    @classmethod
    def generate_passport_issue_date(cls, birthdate: str) -> str:
        return FakeDates.get_passport_issue_date(birthdate)

    # FIXME
    def generate_passport_issuer_code(self) -> str:
        return self.random.generate_string_by_mask(mask="###-###", digit="#")

    def generate_passport_issuer_name(self) -> str:
        return f"Отделом УФМС России по городу {self.address.city()}"

    def generate_birthplace(self) -> str:
        return self.address.country()

    # FIXME
    def generate_snils(self) -> str:
        return self.ru.snils()

    @classmethod
    def generate_address_reg_city(cls) -> str:
        return "Нижний"

    @classmethod
    def generate_address_reg_street(cls) -> str:
        return "Красная"

    @classmethod
    def generate_address_reg_house(cls) -> str:
        return "дом 1"

    @classmethod
    def generate_address_reg_flat(cls) -> str:
        return "1"

    @classmethod
    def generate_address_fact_city(cls) -> str:
        return "Нижний"

    @classmethod
    def generate_address_fact_street(cls) -> str:
        return "Красная"

    @classmethod
    def generate_address_fact_house(cls) -> str:
        return "дом 1"

    @classmethod
    def generate_address_fact_flat(cls) -> str:
        return "1"

    @staticmethod
    def generate_job_type(return_id: bool = True) -> str:
        job_types = {
            "161": "Работаю на себя",
            "28": "Подработка",
            "158": "Пенсионер работающий на ставку",
            "160": "Самозанятый",
            "27": "По договору",
            "26": "Полная",
            "159": "Декрет",
            "157": "Пенсионер",
            "29": "Совместительство",
            "171": "Индивидуальный предприниматель",
            "497": "Не работаю",
        }

        if return_id:
            return random.choice(list(job_types.keys()))
        else:
            return random.choice(list(job_types.values()))

    def generate_job_company_name(self) -> str:
        return self.fin.company()

    def generate_job_company_title(self) -> str:
        return self.person.occupation()

    def generate_salary(self) -> str:
        return str(self.numeric.integer_number(start=10_000, end=999_999))

    def generate_expenses(self) -> str:
        return str(self.numeric.integer_number(start=10_000, end=999_999))

    def generate_amount(self, range_amount: list[int]) -> str:
        min_amount, max_amount = range_amount
        return str(self.numeric.integer_number(start=min_amount, end=max_amount))

    def generate_period(self, period_range: list[int], in_weeks: bool = False) -> str:
        min_period, max_period = period_range
        period = self.numeric.integer_number(start=min_period, end=max_period)
        if in_weeks:
            period /= 7
        return str(period)

    def generate_friend_fio(self) -> str:
        return self.person.full_name(gender=self.gender)

    # TODO можно ли определять провайдера по ссылке в iframe -> shadowDom?
    @classmethod
    def generate_pan(cls, provider: str = "ALFA"):
        if provider == "ALFA":
            return acquiring.alfa_card_pan
        elif provider == "TKB":
            tkb_pans = [card.strip() for card in acquiring.tkb_card_pans.split(",")]
            return random.choice(tkb_pans)
