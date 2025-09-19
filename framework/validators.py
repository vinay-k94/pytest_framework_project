import uuid
from framework.errors import ValidationError


def is_uuid4(val: str) -> bool:
    try:
        u = uuid.UUID(val, version=4)
        return str(u) == val
    except Exception:
        return False


def assert_uuid4(val: str, message: str = "Invalid UUID4"):
    if not is_uuid4(val):
        raise ValidationError(message)


def assert_status_code(resp, expected: int):
    if resp.status_code != expected:
        raise ValidationError(f"Expected status {expected}, got {resp.status_code}: {resp.text}")
