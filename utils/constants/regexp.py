from enum import Enum


class RegExp(str, Enum):
    EMAIL = r"^[0-9A-Za-z_\-]+?[0-9A-Za-z_\-+.]+\.?[0-9A-Za-z_\-+]+@[A-Z-a-z]+\.[A-Z-a-z]{2,6}$"
    INITIALS = r"^[А-ЯЁ][а-яё]*$"
    SMS = r"^[0-9]{6}$"
    JOB_INFO = r"^[0-9а-яёА-ЯЁ\"-’«»„“№ ]{1,127}$"
    PHONE_NUMBER = r"^79\d{9}$"
    PASSPORT_IDENTIFIER = r"^\d{4}\s\d{6}$"
    PASSPORT_ISSUER_CODE = r"^\d{3}-\d{3}$"
    PASSPORT_ISSUER_NAME = r"^[0-9а-яёА-Я- ]{1,127}$"
    SNILS = r"^\d{3}-\d{3}-\d{3}\s\d{2}$"
    BIRTHPLACE = r"^[a-яёА-Я- ]{5,99}$"

    def __str__(self) -> str:
        return self.value
