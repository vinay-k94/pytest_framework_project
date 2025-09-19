import os
from datetime import datetime


def get_report_paths():
    """
    Dynamically generate paths for HTML and Allure reports with timestamp.
    Returns a tuple: (html_report, allure_results_dir)
    """

    # Base reports directory
    base_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(base_dir, exist_ok=True)

    # Subfolders for HTML and Allure
    html_dir = os.path.join(base_dir, "html_reports")
    allure_dir = os.path.join(base_dir, "allure_reports")
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(allure_dir, exist_ok=True)

    # Timestamp for unique reports
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # File paths
    html_report = os.path.join(html_dir, f"report_{timestamp}.html")
    allure_results = os.path.join(allure_dir, f"results_{timestamp}")
    os.makedirs(allure_results, exist_ok=True)

    return html_report, allure_results
