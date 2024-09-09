from __future__ import annotations

from ui.core.driver import Driver
from ui.core.locator import DEFAULT_TIMEOUT, Locator
from typing import List


class Block:
    """Структура для контейнеров, содержащих не уникальные элементы. Позволяет взаимодействовать со всеми элементами.

        container = Block(
            'Example block', '//div',
            title=Locator('Title', '//h1'),
            body=Locator('Body', '//div'),
            field=Input('Value Input', '//input')
        )

    Когда нужен только первый элемент:
        container.field.input('test value')
        container.title.click()

    Когда нужны все элементы:
        for _container in container.get_all_blocks():
            _container.field.input('test value')

    """

    def __init__(self, name: str, xpath: str, **kwargs: {str, Locator}):
        """
        Инициализирует блок с заданным именем и xpath, а также дополнительными локаторами.

        :param name: Имя блока.
        :param xpath: Xpath блока.
        :param kwargs: Дополнительные локаторы в формате {имя: локатор}.
        """
        self._name = name
        self._xpath = xpath
        for _locator_class_name, _locator_object in kwargs.items():
            self.__dict__[_locator_class_name] = _locator_object
        self._update_locators()

    def _update_locators(self):
        """
        Обновляет локаторы блока, добавляя к ним xpath блока и имя блока.
        """
        for value in self.__dict__.values():
            if isinstance(value, Locator):
                value.block_xpath = self._xpath
                value.name = f"[{self._name}] -> {value.name}"

    def get_all_blocks(self) -> List[Block]:
        """
        Возвращает все блоки, соответствующие xpath блока.

        :return: Список всех блоков.
        """
        all_blocks = []
        Driver().page.wait_for_selector(self._xpath, timeout=DEFAULT_TIMEOUT)

        for element in Driver().page.locator(self._xpath).all():
            block = self.__class__(self._name, self._xpath, _webelement=element)

            # добавляет локаторы в новый блок
            for name, value in self.__dict__.items():
                if isinstance(value, Locator):
                    _locator = value.__class__(
                        f"[{block._name}] -> {value.name}", value.xpath
                    )
                    _locator.parent = element
                    block.__dict__[name] = _locator
            all_blocks.append(block)
        return all_blocks

    @staticmethod
    def input_all_blocks(fields, values):
        """
        Вводит значения во все блоки.

        :param fields: Поля для ввода.
        :param values: Значения для ввода.
        """
        specific_fields = ["Населенный пункт", "Улица", "Дом"]

        for value, field in zip(values, fields):
            if any(sf in field.name for sf in specific_fields):
                field.press_sequentially(value, delay=100)
                Driver().page.locator(
                    '(//ul[contains(@id, "address")]//li)[1]'
                ).first.click()
            else:
                field.press_sequentially(value)
