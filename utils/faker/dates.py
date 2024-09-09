from datetime import datetime, date, timedelta
from random import randint

from settings.base import base_settings

DATE_TIME_FORMAT = '%d.%m.%Y'


class FakeDates:
    @staticmethod
    def get_random_birthdate() -> str:
        test_user = base_settings.test_user

        current_date = datetime.now()

        min_days = (current_date - timedelta(days=test_user.max_age * 365)).date()
        max_days = (current_date - timedelta(days=test_user.min_age * 365)).date()

        random_birthdate = datetime.combine(
            date.fromordinal(randint(min_days.toordinal(),
                                     max_days.toordinal())),
            datetime.min.time())

        return random_birthdate.strftime(DATE_TIME_FORMAT)

    @staticmethod
    def get_passport_issue_date(birthdate: str) -> str:
        date_object = datetime.strptime(birthdate, DATE_TIME_FORMAT)
        new_date = date_object.replace(year=date_object.year + 18).strftime(DATE_TIME_FORMAT)

        return new_date
