import os
from dotenv import load_dotenv
load_dotenv()

AUTH_CONFIG = {
    "dashboard": {
        "token_url": os.getenv("DASHBOARD_TOKEN_URL"),
        "client_id": os.getenv("DASHBOARD_CLIENT_ID"),
        "client_secret": os.getenv("DASHBOARD_CLIENT_SECRET"),
    },
    "internal": {
        "token_url": os.getenv("INTERNAL_TOKEN_URL"),
    },
    "oSeries": {
        "token_url": os.getenv("OSERIES_TOKEN_URL"),
    },
}


