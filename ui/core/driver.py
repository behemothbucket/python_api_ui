import os

import allure
from playwright.sync_api import sync_playwright


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Driver(metaclass=Singleton):

    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

        headless_mode = self.config.driver.headless_mode
        desktop_device = self.config.driver.desktop_device
        mobile_device = self.config.driver.mobile_device

        self._playwright = sync_playwright().start()

        if self.config.driver.mobile_mode:
            self.browser = self._playwright.webkit.launch(headless=headless_mode)
            parameters = self._playwright.devices[mobile_device]
        else:
            self.browser = self._playwright.chromium.launch(headless=headless_mode)
            parameters = self._playwright.devices[desktop_device]
            parameters["viewport"] = {
                "width": self.config.viewport.width,
                "height": self.config.viewport.height,
            }

        self.page = self.browser.new_page(**parameters)

    def quit(self):
        self.browser.close()
        self._playwright.stop()

    def switch_to_tab(self, tab_index: int):
        self.page = self.browser.contexts[0].pages[tab_index]

    def attach_screenshot(self, test_name: str):
        screenshots_dir = self.config.logging.screenshots_dir

        if not os.path.exists(screenshots_dir):
            os.mkdir(screenshots_dir)

        screenshot = f"screenshots/{test_name}.png"

        self.page.screenshot(path=screenshot)

        allure.attach.file(
            screenshot, name=test_name, attachment_type=allure.attachment_type.PNG
        )
