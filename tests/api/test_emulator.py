import allure
import pytest

from api.base.api.emulator import Emulator
from utils.constants.qa_annotations import Suite, Tasks


@pytest.mark.api
@pytest.mark.emulator
@allure.feature("emulator")
@allure.story("emulator")
@allure.severity(allure.severity_level.CRITICAL)
@allure.parent_suite(Suite.SMOKE)
@allure.suite(Suite.API)
@allure.link(Tasks.MAIN_TASK)
class TestEmulator:

    @allure.title("Удаление пользователя")
    @allure.tag("api", "smoke")
    @pytest.mark.skip
    def test_delete_person(self, api_client: Emulator):
        phone = "79749642820"  # FIXME

        api_client.get_delete(phone=phone)
