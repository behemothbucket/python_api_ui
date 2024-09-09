import time
from http import HTTPStatus

import allure

from api.models.emulator.delete import DeleteResponse
from api.utils.assertions.base.solutions import assert_status_code
from api.utils.assertions.client_interface import assert_submit_payment
from api.utils.assertions.emulator import assert_delete
from api.utils.clients.http.client import APIClient
from api.utils.constants.routes import APIRoutes
from settings.base import base_settings
from utils.logger import log_response


class Emulator(APIClient):
    base_url = base_settings.api.base_url_emulator

    @allure.step("GET ***")
    def get_delete(self, phone: str):
        params = {"phone": phone}

        response = self.client.get(APIRoutes.DELETE, params=params)
        url = response.url
        data = response.json()

        log_response("GET", url, params, data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_delete(DeleteResponse(), data)

    @allure.step("POST ***")
    def post_submit_payment(self, pan: str, request_id: str) -> "Emulator":
        params = {"amount": "1", "requestId": request_id, "pan": pan}

        response = self.client.post(APIRoutes.SUBMIT_PAYMENT, params=params)

        url = response.url
        data = response.text

        log_response("POST", url, response=data)

        expected_response = (
            "ResultMessage(result=success, message=wait for callback, codeResult=null)"
        )

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_submit_payment(expected_response, data)

        time.sleep(2)  # Убрать если будет нормально работать

        return self

    @allure.step("POST ***")
    def post_prolongation(self):
        pass

    @allure.step("POST ***")
    def post_approve(self):
        pass

    @allure.step("GET ***")
    def get_sber_payment(self):
        pass

    @allure.step("GET ***")
    def get_sber_check(self):
        pass
