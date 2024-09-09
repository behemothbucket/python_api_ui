import allure
import pytest

from api.base.api.client_interface import ClientInterface
from api.base.api.emulator import Emulator
from api.base.api.jd_api import JdApi
from api.utils.clients.http.builder import get_http_client
from settings.ui import get_ui_config
from ui.core.driver import Driver


def is_mobile(request: pytest.FixtureRequest) -> bool:
    return any(mark.name == "mobile" for mark in request.node.own_markers)


@pytest.fixture
def driver(request: pytest.FixtureRequest):
    config = get_ui_config()

    with allure.step("Driver setup"):
        config.driver.mobile_mode = is_mobile(request)
        webdriver = Driver(config=config)

    print()  # start log from new line

    yield webdriver

    if config.logging.screenshots_enabled:
        webdriver.attach_screenshot(request.node.name)

    with allure.step("Driver teardown"):
        try:
            webdriver.quit()
        finally:
            webdriver.__class__._instances = {}


@pytest.fixture(scope="class")
def api_clients():
    client_interface = ClientInterface(
        client=get_http_client(base_url=ClientInterface.base_url)
    )
    jd_api = JdApi(client=get_http_client(base_url=JdApi.base_url))
    emulator = Emulator(client=get_http_client(base_url=Emulator.base_url))

    return client_interface, jd_api, emulator
