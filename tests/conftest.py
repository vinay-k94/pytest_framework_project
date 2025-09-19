import pytest
import datetime
from framework.ui.driver import create_driver
from framework.api_dictionary import ApiDictionary
from config.config_manager import ConfigManager
from datetime import datetime
from framework.report_manager import get_report_paths
from framework.logger import get_logger
import os
import subprocess

logger = get_logger(__name__)


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help="Environment to run tests against (dev, qa, prod)")


@pytest.fixture(scope="session")
def api(request):
    env = request.config.getoption("--env")
    os.environ["ENV"] = env
    config = ConfigManager(env).get_config()
    dictionary = ApiDictionary(
        base_url=config["base_url"],
        auth_type=config.get("auth_type", "none")
    )
    return dictionary


@pytest.fixture(scope="function")
def driver():
    d = create_driver(headless=bool(int(os.getenv("HEADLESS", "1"))))
    yield d
    try:
        d.quit()
    except Exception:
        pass


# def get_timestamped_report_path(report_dir: str = "reports", prefix: str = "report") -> str:
#     """
#     Returns a full path for a timestamped HTML report.
#
#     Args:
#         report_dir (str): Folder where reports will be stored.
#         prefix (str): Prefix for the report file name.
#
#     Returns:
#         str: Full path to the timestamped report file.
#     """
#     # Ensure the report directory exists
#     os.makedirs(report_dir, exist_ok=True)
#
#     # Generate timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#
#     # Full report path
#     report_file = os.path.join(report_dir, f"{prefix}_{timestamp}.html")
#     return report_file


html_report, allure_results = get_report_paths()


def pytest_configure(config):
    # Configure HTML & Allure results paths
    if hasattr(config.option, "htmlpath"):
        config.option.htmlpath = html_report
    if hasattr(config.option, "allure_report_dir"):
        config.option.allure_report_dir = allure_results
    elif hasattr(config.option, "allure_reportdir"):
        config.option.allure_reportdir = allure_results


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session):
    """Generate pretty Allure report automatically after tests."""
    env = session.config.getoption("--env")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_report_dir = os.path.join("reports", "allure_reports", f"allure_{env}_{timestamp}")
    os.makedirs(final_report_dir, exist_ok=True)

    # ✅ Use full path to allure.bat (works even if PATH is not set correctly)
    allure_cmd = r"C:\Users\admin\Downloads\allure-2.29.0\bin\allure.bat"

    try:
        subprocess.run(
            [allure_cmd, "generate", allure_results, "-o", final_report_dir, "--clean"],
            check=True,
        )
        session.config.pluginmanager.get_plugin("terminalreporter").write_line(
            f"\n📊 Allure report generated: {os.path.abspath(final_report_dir)}"
        )
    except Exception as e:
        session.config.pluginmanager.get_plugin("terminalreporter").write_line(
            f"\n⚠️ Failed to generate Allure report automatically: {e}"
        )
