import allure
from selenium.common.exceptions import JavascriptException

from ui.core.decorators import wait_until
from ui.core.driver import Driver


@allure.step("Ожидание перехода страницы на новую страницу")
def wait_for_page_to_change():
    @wait_until()
    def check_if_page_changed():
        try:
            Driver().page.evaluate("return oldPage;")
            return False
        except JavascriptException:
            return True

    check_if_page_changed()


@allure.step("Ожидание полной загрузки страницы")
def wait_for_page_to_load():
    @wait_until()
    def check_page_dom_state():
        page_current_state = Driver().page.evaluate("return document.readyState;")
        if page_current_state == "complete":
            return True
        else:
            return False

    check_page_dom_state()
