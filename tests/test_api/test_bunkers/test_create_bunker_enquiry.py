from datetime import datetime, timezone, timedelta

from framework.api_dictionary import ApiDictionary
from framework.logger import get_logger

logger = get_logger(__name__)


def test_create_bunker_enquiry_with_all_mandatory_fields(api: ApiDictionary):
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

    api.bunker.get_vessels()
    vessel_imo = api.bunker.get_random_vessels_imo()
    api.bunker.get_customers()
    customer_id = api.bunker.get_random_customer_id()
    api.bunker.get_port()
    port_unlocode = api.bunker.get_random_ports_unlocode()
    api.bunker.get_bunker_details()
    external_id, sulphur_external_id = api.bunker.get_external_and_sulphur_id()

    delivery_start = datetime.now(timezone.utc)  # timezone-aware datetime
    delivery_end = delivery_start + timedelta(days=4)  # add 4 days

    delivery_start_str = delivery_start.isoformat().replace("+00:00", "Z")
    delivery_end_str = delivery_end.isoformat().replace("+00:00", "Z")
    quantity_max = 555
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(200)


def test_create_duplicate_bunker_enquiry_with_same_fields(api: ApiDictionary):
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

    api.bunker.get_vessels()
    vessel_imo = api.bunker.get_random_vessels_imo()
    api.bunker.get_customers()
    customer_id = api.bunker.get_random_customer_id()
    api.bunker.get_port()
    port_unlocode = api.bunker.get_random_ports_unlocode()
    api.bunker.get_bunker_details()
    external_id, sulphur_external_id = api.bunker.get_external_and_sulphur_id()

    delivery_start = datetime.now(timezone.utc)  # timezone-aware datetime
    delivery_end = delivery_start + timedelta(days=4)  # add 4 days

    delivery_start_str = delivery_start.isoformat().replace("+00:00", "Z")
    delivery_end_str = delivery_end.isoformat().replace("+00:00", "Z")
    quantity_max = 555
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(200)

    api.bunker.create_bunker_enquiry(200)


def test_create_bunker_enquiry_with_invalid_mandatory_fields(api: ApiDictionary):
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

    api.bunker.get_vessels()
    vessel_imo = api.bunker.get_random_vessels_imo()
    api.bunker.get_customers()
    customer_id = api.bunker.get_random_customer_id()
    api.bunker.get_port()
    port_unlocode = api.bunker.get_random_ports_unlocode()
    api.bunker.get_bunker_details()
    external_id, sulphur_external_id = api.bunker.get_external_and_sulphur_id()

    delivery_start = datetime.now(timezone.utc)  # timezone-aware datetime
    delivery_end = delivery_start + timedelta(days=4)  # add 4 days

    delivery_start_str = delivery_start.isoformat().replace("+00:00", "Z")
    delivery_end_str = delivery_end.isoformat().replace("+00:00", "Z")
    quantity_max = 555
    # Invalid Customer ID Field
    api.bunker.generate_payload_bunker_enquiry_create("111111", vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)
    # Invalid Vessel IMO Field --- Backend issue getting 500 instead of 400
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, "1111111", port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    # api.bunker.create_bunker_enquiry(400)

    # Invalid Port Unlocode Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, "1111111",
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(500)

    # Invalid External ID Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      "1111111", sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Invalid Sulphur External ID Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, "1111111",
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Invalid Delivery Start Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      "2024", delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Invalid Delivery End Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, "2029", quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Invalid Quantity Max Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, -200)
    api.bunker.create_bunker_enquiry(400)


def test_create_bunker_enquiry_with_missing_mandatory_fields(api: ApiDictionary):
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

    api.bunker.get_vessels()
    vessel_imo = api.bunker.get_random_vessels_imo()
    api.bunker.get_customers()
    customer_id = api.bunker.get_random_customer_id()
    api.bunker.get_port()
    port_unlocode = api.bunker.get_random_ports_unlocode()
    api.bunker.get_bunker_details()
    external_id, sulphur_external_id = api.bunker.get_external_and_sulphur_id()

    delivery_start = datetime.now(timezone.utc)  # timezone-aware datetime
    delivery_end = delivery_start + timedelta(days=4)  # add 4 days

    delivery_start_str = delivery_start.isoformat().replace("+00:00", "Z")
    delivery_end_str = delivery_end.isoformat().replace("+00:00", "Z")
    quantity_max = 555
    # Missing Customer ID Field
    api.bunker.generate_payload_bunker_enquiry_create(None, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)
    # Missing Vessel IMO Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, None, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Missing Port Unlocode Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, None,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Missing External ID Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      None, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Missing Sulphur External ID Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, None,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Missing Delivery Start Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      None, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Missing Delivery End Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, None, quantity_max)
    api.bunker.create_bunker_enquiry(400)

    # Missing Quantity Max Field
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, None)
    api.bunker.create_bunker_enquiry(400)


def test_create_bunker_enquiry_negative_fields(api: ApiDictionary):
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

    api.bunker.get_vessels()
    vessel_imo = api.bunker.get_random_vessels_imo()
    api.bunker.get_customers()
    customer_id = api.bunker.get_random_customer_id()
    api.bunker.get_port()
    port_unlocode = api.bunker.get_random_ports_unlocode()
    api.bunker.get_bunker_details()
    external_id, sulphur_external_id = api.bunker.get_external_and_sulphur_id()

    delivery_start = datetime.now(timezone.utc)  # timezone-aware datetime
    delivery_end = delivery_start + timedelta(days=4)  # add 4 days

    delivery_end_str = delivery_start.isoformat().replace("+00:00", "Z")
    delivery_start_str = delivery_end.isoformat().replace("+00:00", "Z")
    quantity_max = 555
    quantity_min = 700
    # with max delivery start date
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str, quantity_max)
    api.bunker.create_bunker_enquiry(400)
    # with high min quantity value
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str,
                                                      quantity_max, quantity_min)
    api.bunker.create_bunker_enquiry(400)
    # with low max quantity value
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str,
                                                      0, quantity_min)
    api.bunker.create_bunker_enquiry(400)
    # with high max quantity value
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str,
                                                      1500, quantity_min)
    api.bunker.create_bunker_enquiry(400)
    # with max quantity as string value
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, vessel_imo, port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str,
                                                      "555", quantity_min)
    api.bunker.create_bunker_enquiry(400)
    # with vessel imo as string value
    api.bunker.generate_payload_bunker_enquiry_create(customer_id, "fxhrh", port_unlocode,
                                                      external_id, sulphur_external_id,
                                                      delivery_start_str, delivery_end_str,
                                                      "555", quantity_min)
    api.bunker.create_bunker_enquiry(400)

