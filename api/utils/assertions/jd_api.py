from pydantic import BaseModel

from api.models.jd_api.apply_offer import ApplyOfferSuccessResponse
from api.utils.assertions.base.expect import expect


def assert_apply_offer(expected_response: BaseModel, actual_response: ApplyOfferSuccessResponse):
    expect(expected_response.timestamp) \
        .set_description('Field "timestamp"') \
        .to_be_equal(actual_response['timestamp'])

    expect(expected_response.success) \
        .set_description('Field "success"') \
        .to_be_equal(actual_response['success'])

    expect(expected_response.response) \
        .set_description('Field "response"') \
        .to_be_equal(actual_response['response'])
