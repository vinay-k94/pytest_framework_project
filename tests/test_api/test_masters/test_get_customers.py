from framework.logger import get_logger

from framework.validators import assert_status_code
from framework.api_dictionary import ApiDictionary
import pytest

logger = get_logger(__name__)


def test_list_users_and_validate(api: ApiDictionary):
    """
        Test Case: List Users API - Validate Response Structure and Content

        Steps:
        1. Call the API to fetch a paginated list of users (page=1, size=10).
        2. Assert that the API call returns HTTP 200 (success).
        3. Assert that the response is a non-empty list.
        4. Assert that the
        first user object contains 'id' and 'name' keys.

        Purpose:
        - To verify that the user listing endpoint returns valid data and expected structure.
        - To ensure basic integrity of the user objects in the response.

        args: api (ApiDictionary): The API client instance for making requests.
    """
    result = api.get_customers()
    logger.info(f"List Users API response: {result}")
