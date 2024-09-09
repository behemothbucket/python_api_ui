from typing import List

import allure

from ui.core.driver import Driver
from ui.core.locator import Locator
from ui.utils.constants.routes import UIRoutes
from utils.logger import logger


class Page:
    """
    Main class for pages, contains locators
    """

    def open(self):
        with allure.step(f'Открыть страницу {self.__class__.__name__}'):
            logger.info(f'Открыть страницу {self.__class__.__name__}')
            Driver().page.goto(UIRoutes.LOGIN_PAGE, wait_until='domcontentloaded')
            return self

    def wait_for_url(self, url: str):
        with allure.step(f'Дождаться страницы {url}'):
            logger.info(f'Дождаться страницы {url}')
            Driver().page.wait_for_url(url, timeout=16_000)
            return self

    def open_with_path(self, path: str):
        with allure.step(f'Открыть страницу {self.__class__.__name__} по пути path={path}'):
            Driver().page.goto(UIRoutes.BASE_URL + path)
            return self

    def pause(self):
        with allure.step('Драйвер на паузе...'):
            logger.info('Драйвер на паузе...')
            Driver().page.pause()
            return self

    @staticmethod
    def reload():
        with allure.step('Перезагрузить страницу'):
            logger.info('Перезагрузить страницу')
            Driver().page.reload()

    @staticmethod
    def current_url() -> str:
        with allure.step('Получить текущий URL'):
            logger.info('Получить текущий URL')
            return Driver().page.url

    @staticmethod
    def evaluate(script: str):
        with allure.step(f'Исполнить JS скрипт {script}'):
            logger.info(f'Исполнить JS скрипт {script}')
            try:
                Driver().page.evaluate(script)
            except Exception as e:
                logger.error(e)

    @staticmethod
    def file_chooser_upload(*path: List[str], element: Locator):
        with Driver().page.expect_file_chooser() as fc_info:
            element.click()
        file_chooser = fc_info.value

        if file_chooser.is_multiple():
            file_chooser.set_files(*path)
        else:
            file_chooser.set_files(path[0])

    @staticmethod
    def press_key(key: str):
        with allure.step(f'Нажать на клавишу {key}'):
            logger.info(f'Нажать на клавишу {key}')
            Driver().page.keyboard.press(key)
