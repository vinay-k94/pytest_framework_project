# Pytest + Selenium API & UI Automation Framework (Enterprise Scaffold)

This repository is a scaffold for an enterprise-ready automation framework using:
- Python 3
- pytest
- requests
- selenium
- PyJWT
- python-dotenv

Structure and core components are included: ApiClient, Dictionary (endpoint registry),
TokenManager, validators, Selenium Page Objects, fixtures, and sample tests.

## How to use
1. Copy `.env.example` to `.env` and fill in real endpoint/credentials.
2. Create virtualenv and install requirements: `python -m pip install -r requirements.txt`
3. Run tests: `pytest -q`

See `tests/` for sample API and UI tests.
