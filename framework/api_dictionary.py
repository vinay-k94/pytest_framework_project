from typing import Dict
from framework.api_client import ApiClient
from framework.errors import ApiError
from framework.logger import get_logger   # import central logger
from tests.api.bunker import Bunker

logger = get_logger(__name__)   # logger for this class


class EndPoints:
    GET_CUSTOMERS = "/api/customers"
    GET_DA_LIST = "/api/da/list"


class ApiDictionary:
    def __init__(self, base_url: str, auth_type: str = "none"):
        self.client = ApiClient(base_url=base_url, auth_type=auth_type)
        self.bunker = Bunker(client=self.client)
        self.last_response = None   # keep track of last API response
        self.last_json = None
        self.get_customers_response = {}
        self.get_da_list_response = {}

    def get_customers(self):
        self.get_customers_response = self.client.get(EndPoints.GET_CUSTOMERS)
        self.last_response = self.get_customers_response
        logger.info(f"Response: {self.last_response.status_code}")
        return self.last_response

    def get_da_list(self):
        self.get_da_list_response = self.client.get(EndPoints.GET_DA_LIST)
        self.last_response = self.get_da_list_response
        logger.info(f"DA Response: {self.last_response.status_code}")
        return self.last_response

    def _fetch_last_json(self) -> Dict:
        """Helper to fetch and cache the last JSON response."""
        if self.last_response is None:
            error_msg = "No API call has been made yet"
            logger.error(error_msg)
            raise ApiError(error_msg)
        try:
            self.last_json = self.last_response.json()
            logger.debug(f"Fetched last JSON: {self.last_json}")
            return self.last_json
        except Exception as e:
            error_msg = f"Failed to parse JSON from last response: {e}"
            logger.error(error_msg)
            raise ApiError(error_msg)
