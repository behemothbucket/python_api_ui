import time
from http import HTTPStatus

import allure

from api.models.jd_api.apply_offer import (ApplyOfferPayload,
                                           ApplyOfferSuccessResponse)
from api.utils.assertions.base.solutions import assert_status_code
from api.utils.assertions.jd_api import assert_apply_offer
from api.utils.assertions.schema import validate_schema
from api.utils.clients.http.client import APIClient
from api.utils.constants.routes import APIRoutes
from settings.base import base_settings
from utils.logger import log_response


class JdApi(APIClient):
    base_url = base_settings.api.base_url_jd_api

    @allure.step("POST ***")
    def post_apply_offer(self, **kwargs):
        application_id = kwargs.get("application_id")
        amount = kwargs.get("amount")
        days = kwargs.get("days")
        tariff_id = kwargs.get("tariff_id")
        staff_id = kwargs.get("staff_id", 2000)

        payload = ApplyOfferPayload(
            applicationId=application_id,
            amount=amount,
            days=days,
            tariffId=tariff_id,
            staffId=staff_id,
        )

        # TODO Сделать проверку ожидания СПР

        time.sleep(30)

        response = self.client.post(APIRoutes.APPLY_OFFER, json=payload.model_dump())
        url = response.url
        data = response.json()

        timestamp = data["timestamp"]

        log_response("POST", url, payload.model_dump(), data)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_apply_offer(ApplyOfferSuccessResponse(timestamp=timestamp), data)

        validate_schema(data, ApplyOfferSuccessResponse.model_json_schema())

        return self
