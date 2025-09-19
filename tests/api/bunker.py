import logging
from typing import Dict
from framework.api_client import ApiClient
from framework.errors import ApiError
from framework.logger import get_logger  # import central logger
import random
from framework.validators import assert_status_code
from datetime import datetime, timedelta, timezone
from typing import Tuple

logger = get_logger(__name__)  # logger for this class


class EndPoints:
    GET_CUSTOMERS = "/api/customers"
    GET_VESSELS = "/api/my-fleet"
    GET_PORTS = "/api/ports"
    GET_AGENTS = "/api/agents"
    GET_BUNKER_DETAILS = "/api/fuel-sulphur-iso"
    GET_BUNKER_ENQUIRIES = "/api/bunker/create-inquiry"


class Bunker:
    def __init__(self, client: ApiClient):
        self.client = client
        self.last_response = None  # keep track of last API response
        self.last_json = None
        self.get_customers_response = {}
        self.get_vessels_response = {}
        self.get_port_response = {}
        self.get_agent_response = {}
        self.get_bunker_details_response = {}
        self.create_bunker_enquiry_response = {}
        self.bunker_enquiry_create_payload = {}

    def _fetch_last_json(self) -> dict | list:
        """Helper to fetch and cache the last JSON response."""
        if self.last_response is None:
            raise ApiError("No API call has been made yet")
        try:
            raw = self.last_response.json()
            # If response is dict and has "data", unwrap it
            if isinstance(raw, dict) and "data" in raw:
                self.last_json = raw["data"]
            else:
                self.last_json = raw
            return self.last_json
        except Exception as e:
            raise ApiError(f"Failed to parse JSON from last response: {e}")

    def get_customers(self):
        self.last_response = self.client.get(EndPoints.GET_CUSTOMERS)
        self.get_customers_response = self._fetch_last_json()
        logger.info(f"Response: {self.last_response.status_code}")

    def get_vessels(self):
        self.last_response = self.client.get(EndPoints.GET_VESSELS)
        self.get_vessels_response = self._fetch_last_json()
        logger.info(f"Response: {self.last_response.status_code}")

    def get_port(self):
        self.last_response = self.client.get(EndPoints.GET_PORTS)
        self.get_port_response = self._fetch_last_json()
        logger.info(f"Response: {self.last_response.status_code}")

    def get_agents(self):
        self.last_response = self.client.get(EndPoints.GET_AGENTS)
        self.get_agent_response = self._fetch_last_json()
        logger.info(f"Response: {self.last_response.status_code}")

    def get_bunker_details(self):
        self.last_response = self.client.get(EndPoints.GET_BUNKER_DETAILS)
        self.get_bunker_details_response = (self._fetch_last_json())['fuels']
        logger.info(f"Response: {self.last_response.status_code}")

    def get_random_customer_id(self):
        customer = random.choice(self.get_customers_response)
        return customer['external_id']

    def get_random_vessels_imo(self):
        vessels = random.choice(self.get_vessels_response)
        return vessels['imo']

    def get_random_ports_unlocode(self):
        ports = random.choice(self.get_port_response)
        return ports['unlocode']

    def get_external_and_sulphur_id(self) -> tuple[str, str]:
        fuel = random.choice(self.get_bunker_details_response)
        external_id = fuel["external_id"]
        sulphur_external_id = fuel["sulphurs"][0]["external_id"]
        return external_id, sulphur_external_id

    def generate_payload_bunker_enquiry_create(self, customer_id: str, vessel_imo: int, port_unlocode: str,
                                               fuel_id: str, sulphur_id: str, delivery_start: str,
                                               delivery_end: str, quantity_max: int, quantity_min: int = None):

        self.bunker_enquiry_create_payload = {
            "customer_id": customer_id,
            "vessel_imo": vessel_imo,
            "port_unlocode": port_unlocode,
            "delivery_start_date": delivery_start,
            "delivery_end_date": delivery_end,
            "fuels": [
                {
                    "external_id": fuel_id,
                    "sulphur_external_id": sulphur_id,
                    "quantity_min": quantity_min,
                    "quantity_max": quantity_max
                }
            ]
        }

    def create_bunker_enquiry(self, expected_status: int):
        if not self.bunker_enquiry_create_payload:
            raise ApiError("Bunker enquiry payload is empty. Generate it first.")
        logger.info(self.bunker_enquiry_create_payload)
        self.last_response = self.client.post(
            EndPoints.GET_BUNKER_ENQUIRIES, json=self.bunker_enquiry_create_payload
        )
        assert_status_code(self.last_response, expected_status)
        logger.info(f"Response: {self.last_response.status_code}")
        self.create_bunker_enquiry_response = self._fetch_last_json()
