from __future__ import annotations

import re
from typing import Union

import allure
from playwright.sync_api import Locator as PlaywrightLocator

from settings.base import base_settings
from ui.core.driver import Driver
from ui.core.exceptions import CustomBrokenException
from utils.logger import logger

DEFAULT_TIMEOUT = base_settings.driver.default_timeout


class Locator:
    """Локатор элемента на странице."""

    name: str = ""  # переопределено в классе Block
    xpath: str = None
    block_xpath: str = ""  # переопределено в классе Block
    parent: PlaywrightLocator = None  # переопределено в классе Block
    web_element: PlaywrightLocator = None

    def __init__(self, name: str, xpath: str):
        self.xpath = xpath
        self.name = name
        # self.web_element = Driver().page.locator(self.block_xpath + self.xpath)

    def _use_current_page_context(self):
        """Обновить web_element в контексте текущей страницы."""

        if self.parent:
            self.web_element = self.parent.locator(self.block_xpath + self.xpath)
        else:
            self.web_element = Driver().page.locator(self.block_xpath + self.xpath)

    def click(self, wait_for_new_tab: bool = False, force: bool = False):
        """Кликнуть по элементу

        Args:
            wait_for_new_tab: Подождать когда откроется ссылка в новой вкладке и перейти на новую вкладку.
            force: Принудительный клик.

        """

        self._use_current_page_context()

        with allure.step(f"Нажать на {self.name}"):
            logger.info(f"Нажать на {self.name}")
            if force:
                self.web_element.first.click(timeout=DEFAULT_TIMEOUT, force=True)
            # record new opened tab into context
            if wait_for_new_tab:
                with Driver().browser.contexts[0].expect_page() as _:
                    self.web_element.first.click(timeout=DEFAULT_TIMEOUT)
                # update page context to new page
                Driver().switch_to_tab(-1)
            # navigate to another url on the same tab
            else:
                self.web_element.first.click(timeout=DEFAULT_TIMEOUT)

    def text(self, get_number: bool = False):
        """Получить текстовое значение внутри элемента.

        Returns:
            str: Текстовое значение
            int: Числовое значение (если get_number=True)
        """
        self._use_current_page_context()
        text = "".join(self.web_element.first.text_content())
        if get_number:
            return int("".join(re.findall(r"\d", text)))
        return text

    def is_visible(self) -> bool:
        """Проверить, что элемент виден на странице.

        Returns:
            bool: Возвращает True если элемент виден, и False если нет

        """

        self._use_current_page_context()
        with allure.step(f"Проверка элемента: {self.name} на странице"):
            logger.info(f"Проверка элемента: {self.name} на странице")
            self.wait_for_visible(timeout=DEFAULT_TIMEOUT)
            return self.web_element.first.is_visible()

    def get_attribute(self, attribute) -> str:
        """Получить аттрибут элемента.

        Args:
            attribute: Строковое представление аттрибута.

        Returns:
            str: Аттрибут элемента

        """

        self._use_current_page_context()
        return self.web_element.first.get_attribute(attribute, timeout=DEFAULT_TIMEOUT)

    def wait_for_visible(self, timeout=DEFAULT_TIMEOUT):
        """Подождать до появления элемента на странице.

        Видимость означает, что элемент не только отображается,
        но также имеет высоту и ширину больше 0.

        Args:
            timeout: Таймаут ожидания в мс.

        Raises:
            CustomBrokenException

        """

        self._use_current_page_context()
        try:
            self.web_element.first.wait_for(timeout=timeout, state="visible")
        except:
            raise CustomBrokenException(
                f"Элемент {self.name} с xpath={self.block_xpath + self.xpath} не отображен"
            )


class Iframe(Locator):
    name: str = ""
    xpath: str = None
    web_element: PlaywrightLocator = None

    def __init__(self, name: str, xpath: str):
        super().__init__(name, xpath)
        self.xpath = xpath
        self.name = name
        self.web_element = river().page.frame_locator(self.xpath)

    def locator(self, locator: Union[Locator, Input]) -> Union[Locator, Input]:
        xpath = locator.xpath
        return elf.web_element.locator(xpath)


class Input(Locator):
    def input(self, value: str):
        """Ввод значения в поле.

        Args:
            value: Строковое значение

        """

        self._use_current_page_context()
        with allure.step(f"Ввод {value} в {self.name}"):
            logger.info(f"Ввод {value} в {self.name}")
            self.web_element.first.fill(value, timeout=DEFAULT_TIMEOUT)

    @property
    def value(self) -> str:
        """
        Получить значение поля.

        Returns:
            Значение поля

        """

        self._use_current_page_context()
        with allure.step(f"Получить значение из {self.name}"):
            logger.info(f"Получить значение из {self.name}")
            return self.web_element.first.input_value(timeout=DEFAULT_TIMEOUT)

    def focus(self):
        """Перевести фокус на элемент"""

        self._use_current_page_context()
        with allure.step(f"Фокус на {self.name}"):
            logger.info(f"Фокус на {self.name}")
            self.web_element.first.focus()

    def press_sequentially(self, value: str, delay: int = 50):
        """Последовательный ввод символов в поле.

        Полезно, когда у элемента input_mode="numeric".

        Args:
            value: Строковое значение
            delay: Задержка в мс

        """

        self._use_current_page_context()
        with allure.step(f"Ввести последовательно {value} в {self.name}"):
            logger.info(f"Ввести последовательно {value} в {self.name}")
            self.web_element.first.press_sequentially(value, delay=delay)

    def fill(self, value: str):
        """Заполнение поля.

        Полезно, когда у элемента input_mode="numeric".

        Args:
            value: Строковое значение

        """

        self._use_current_page_context()
        with allure.step(f"Ввести {value} в {self.name}"):
            logger.info(f"Ввести {value} в {self.name}")
            self.web_element.first.fill(value)

    def press(self, key: str):
        """Нажатие клавиши на клавиатуре.

        Args:
            key: Клавиша

        """

        self._use_current_page_context()
        with allure.step(f"Нажать кнопку {key} на клавиатуре"):
            logger.info(f"Нажать кнопку {key} на клавиатуре")
            self.web_element.first.press(key)

    def upload_files(self, file_path: str):
        """Загрузка файлов.

        Args:
            file_path: Путь к файлу

        """

        self._use_current_page_context()
        with allure.step("Загрузка фото паспорта..."):
            logger.info("Загрузка фото паспорта...")
            self.web_element.set_input_files([file_path, file_path, file_path])

    def clear(self):
        """Очистка поля."""

        self._use_current_page_context()
        with allure.step("Очистка поля"):
            logger.info("Очистка поля")
            self.web_element.clear()
