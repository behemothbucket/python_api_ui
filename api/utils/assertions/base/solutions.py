from http import HTTPStatus

from api.utils.assertions.base.expect import expect


def assert_status_code(actual: int, expected: HTTPStatus) -> None:
    expect(expected) \
        .set_description('Response status code') \
        .to_be_equal(actual)
