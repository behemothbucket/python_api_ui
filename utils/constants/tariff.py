import random
from itertools import chain


class Tariff:
    FIRST_PDL = 45
    SECOND_PDL = 43
    THIRD_PDL = 44
    FOURTH_PDL = 47

    FIRST_IL = {
        "id": 165,
        "locator": "start",
        "amount_range": [*range(25000, 30001, 500)],
        "period_range": [70],
        "step": 500,
    }

    SECOND_IL = 170
    THIRD_IL = (164, 170)

    MEGA_START = {
        "value": "MEGA_START",
        "locator": "start",
        "amount_range": [*range(3000, 12501, 500)],
        "period_range": [*range(10, 31)],
        "step": 500,
    }

    PRAKTIK = {
        "value": "PRAKTIK",
        "locator": "middle",
        "amount_range": [*range(10000, 30001, 1000)],
        "period_range": [*range(10, 31)],
        "step": 1000,
    }

    PROFI = {
        "value": "PROFI",
        "locator": "end",
        "amount_range": [
            *chain(range(25000, 30001, 1000), range(40000, 100001, 20000))
        ],
        "period_range": [10, 16, 20, 24],
        "step": 20000,
    }

    @classmethod
    def get_tariff_info(cls, tariff_name: str) -> dict:
        """
        Возвращает информацию о тарифе по его имени.

        Args:
            tariff_name (str): Имя тарифа.

        Returns:
            dict: Информация о тарифе.

        Raises:
            ValueError: Если тариф не найден.
        """
        tariff_info = getattr(cls, tariff_name, None)
        if tariff_info is None:
            raise ValueError(f"Тариф '{tariff_name}' не найден.")
        return tariff_info

    @classmethod
    def get_amount_range(cls, tariff_name: str) -> list:
        """
        Возвращает диапазон сумм для указанного тарифа.

        Args:
            tariff_name (str): Имя тарифа.

        Returns:
            list: Диапазон сумм.
        """
        tariff_info = cls.get_tariff_info(tariff_name)
        return tariff_info["amount_range"]

    @classmethod
    def get_period_range(cls, tariff_name: str) -> list:
        """
        Возвращает диапазон периодов для указанного тарифа.

        Args:
            tariff_name (str): Имя тарифа.

        Returns:
            list: Диапазон периодов.
        """
        tariff_info = cls.get_tariff_info(tariff_name)
        return tariff_info["period_range"]

    @classmethod
    def get_step(cls, tariff_name: str) -> int:
        """
        Возвращает шаг для указанного тарифа.

        Args:
            tariff_name (str): Имя тарифа.

        Returns:
            int: Шаг тарифа.
        """
        tariff_info = cls.get_tariff_info(tariff_name)
        return tariff_info["step"]

    @classmethod
    def get_min_max_amount(cls, tariff_name: str) -> tuple[int, int]:
        """
        Возвращает минимальное и максимальное значение из диапазона сумм для указанного тарифа.

        Args:
            tariff_name (str): Имя тарифа.

        Returns:
            tuple[int, int]: Минимальное и максимальное значение.
        """
        amount_range = cls.get_amount_range(tariff_name)
        return min(amount_range), max(amount_range)

    @classmethod
    def get_min_max_period(cls, tariff_name: str) -> tuple[int, int]:
        """
        Возвращает минимальное и максимальное значение из диапазона периодов для указанного тарифа.

        Args:
            tariff_name (str): Имя тарифа.

        Returns:
            tuple[int, int]: Минимальное и максимальное значение.
        """
        period_range = cls.get_period_range(tariff_name)
        return min(period_range), max(period_range)

    @classmethod
    def generate_random_amount(cls, tariff_type):
        """
        Генерирует случайную сумму в пределах диапазона для указанного тарифа.

        Args:
            tariff_type (str): Тип тарифа.

        Returns:
            str: Случайная сумма.
        """
        tariff_config = getattr(cls, tariff_type.upper())
        amount_range = tariff_config["amount_range"]
        min_amount = min(amount_range)
        max_amount = max(amount_range)
        step = tariff_config["step"]
        return str(random.randrange(min_amount, max_amount + 1, step))

    @classmethod
    def generate_random_days(cls, tariff_type):
        """
        Генерирует случайное количество дней в пределах диапазона для указанного тарифа.

        Args:
            tariff_type (str): Тип тарифа.

        Returns:
            str: Случайное количество дней.
        """
        tariff_config = getattr(cls, tariff_type.upper())
        return str(random.choice(tariff_config["period_range"]))
