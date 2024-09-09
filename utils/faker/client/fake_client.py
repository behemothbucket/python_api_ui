import re
from datetime import datetime, timedelta
from typing import List, Any, Set

from pydantic import BaseModel, field_validator
from pydantic import Field, ConfigDict

from settings.base import base_settings
from utils.constants.regexp import RegExp
from utils.faker.client.fake_data import FakeData
from utils.faker.dates import DATE_TIME_FORMAT

test_user = base_settings.test_user
fd = FakeData()


class FakeUser(BaseModel):
    model_config = ConfigDict(validate_default=True)

    phone_number: str = Field(
        default_factory=fd.generate_random_phone_number, pattern=RegExp.PHONE_NUMBER
    )
    name: str = Field(
        default_factory=fd.generate_russian_name,
        min_length=1,
        max_length=40,
        pattern=RegExp.INITIALS,
    )
    surname: str = Field(
        default_factory=fd.generate_russian_surname,
        min_length=1,
        max_length=30,
        pattern=RegExp.INITIALS,
    )
    patronymic: str = Field(
        default_factory=fd.generate_russian_patronymic,
        min_length=1,
        max_length=40,
        pattern=RegExp.INITIALS,
    )
    birthdate: str = Field(default_factory=fd.generate_birthdate)
    email: str = Field(default_factory=fd.generate_email)
    passportIdentifier: str = Field(
        default_factory=fd.generate_passport_issuer_identifier,
        pattern=RegExp.PASSPORT_IDENTIFIER,
        alias="passportIdentifier",
    )
    passportIssueDate: str = Field(default="01.01.2024")  # TODO
    passportIssuerCode: str = Field(
        default_factory=fd.generate_passport_issuer_code,
        pattern=RegExp.PASSPORT_ISSUER_CODE,
    )
    passportIssuerName: str = Field(
        default_factory=fd.generate_passport_issuer_name,
        pattern=RegExp.PASSPORT_ISSUER_NAME,
    )
    birthPlace: str = Field(default="гор Москва", pattern=RegExp.BIRTHPLACE)
    snils: str = Field(default="012-345-678 19", pattern=RegExp.SNILS)
    addressRegCity: str = Field(default_factory=fd.generate_address_reg_city)
    addressRegStreet: str = Field(default_factory=fd.generate_address_reg_street)
    addressRegHouse: str = Field(default_factory=fd.generate_address_reg_house)
    addressRegFlat: str = Field(default_factory=fd.generate_address_reg_flat)
    addressRegId: str = Field(default="4cbce9f3-6fd7-4162-962d-41268b75aadc")
    addressFactCity: str = Field(default_factory=fd.generate_address_fact_city)
    addressFactStreet: str = Field(default_factory=fd.generate_address_fact_street)
    addressFactHouse: str = Field(default_factory=fd.generate_address_fact_house)
    addressFactFlat: str = Field(default_factory=fd.generate_address_fact_flat)
    addressFactId: str = Field(default="4cbce9f3-6fd7-4162-962d-41268b75aadc")
    jobCompanyName: str = Field(
        default_factory=fd.generate_job_company_name, pattern=RegExp.JOB_INFO
    )
    jobType: str = Field(
        default_factory=fd.generate_job_type,
    )
    jobTitle: str = Field(
        default_factory=fd.generate_job_company_title, pattern=RegExp.JOB_INFO
    )
    salary: str = Field(
        default_factory=fd.generate_salary,
    )
    expensesAmount: str = Field(
        default_factory=fd.generate_expenses,
    )
    bankruptcyProcessed: str = Field(default="false")
    friendPhone: str = Field(default="79000000050", pattern=RegExp.PHONE_NUMBER)

    def values(self, exclude: Set[str] = None) -> List[Any]:
        """
        Возвращает список значений полей модели, исключая указанные поля.

        Args:
            exclude (Set[str], optional): Набор имен полей для исключения.

        Returns:
            List[Any]: Список значений полей модели.
        """
        return list(self.model_dump(exclude=exclude).values())

    @classmethod
    @field_validator("email")
    def validate_email(cls, email: str) -> str:
        """
        Проверяет корректность формата email.

        Args:
            email (str): Проверяемый email.

        Raises:
            ValueError: Если формат email неверный.

        Returns:
            str: Проверенный email.
        """
        if not re.match(RegExp.EMAIL, email):
            raise ValueError("Неверный формат email")
        return email

    @staticmethod
    @field_validator("birthdate")
    def validate_dates(date: datetime) -> str:
        """
        Проверяет, что дата рождения соответствует допустимому возрастному диапазону.

        Args:
            date (datetime): Дата рождения для проверки.

        Raises:
            ValueError: Если возраст не входит в допустимый диапазон.

        Returns:
            str: Отформатированная дата рождения.
        """
        max_age = test_user.max_age
        min_age = test_user.min_age

        min_year = datetime.today() - timedelta(days=365 * max_age)
        max_year = datetime.today() - timedelta(days=365 * min_age)

        if date < min_year or date > max_year:
            raise ValueError(
                f"Возраст клиента должен быть между {min_age} и {max_age} годами включительно"
            )

        return date.strftime(DATE_TIME_FORMAT)

    @staticmethod
    @field_validator("salary", "expensesAmount")
    def validate_salary_expenses(value: str) -> str:
        """
        Проверяет, что значение зарплаты или расходов находится в допустимом диапазоне.

        Args:
            value (str): Проверяемое значение.

        Raises:
            ValueError: Если значение выходит за допустимые пределы.

        Returns:
            str: Проверенное значение.
        """
        min_number = test_user.min_salary_expenses
        max_number = test_user.max_salary_expenses

        if not min_number <= int(value) <= max_number:
            raise ValueError(
                f"Значение должно быть от {min_number} до {max_number} включительно"
            )

        return value

    def model_dump_api(self) -> dict:
        """
        Возвращает словарь с данными модели для API, исключая определенные поля.

        Returns:
            dict: Словарь с данными модели без исключенных полей.
        """
        return self.model_dump(
            exclude={
                "name",
                "phone_number",
                "addressRegCity",
                "addressRegStreet",
                "addressFactCity",
                "addressFactStreet",
            }
        )
