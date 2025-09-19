from framework.logger import get_logger
import os
import json


logger = get_logger(__name__)


class ConfigManager:
    """
    Loads environment-specific configuration from the /config directory.
    Example: uat.json, test.json, prod.json
    """

    def __init__(self, env: str = None):
        # Read from ENV variable if not passed explicitly
        self.env = env or os.getenv("ENV", "test")
        base_path = os.path.join(os.path.dirname(__file__), "..", "config")
        self.config_path = os.path.abspath(os.path.join(base_path, f"{self.env}.json"))
        logger.info(f"Loading config for environment '{self.env}' from {self.config_path}")

        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Config file not found for environment '{self.env}': {self.config_path}"
            )

        with open(self.config_path, "r") as f:
            self.config = json.load(f)

    def get(self, key: str, default=None):
        """Get a specific config value."""
        return self.config.get(key, default)

    def get_config(self) -> dict:
        """Return the entire config dictionary."""
        return self.config
