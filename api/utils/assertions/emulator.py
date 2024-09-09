from pydantic import BaseModel

from api.utils.assertions.base.expect import expect


def assert_delete(expected_response: BaseModel, actual_response: bool):
    expect(expected_response.success) \
        .set_description('Success true/false') \
        .to_be_equal(actual_response)
