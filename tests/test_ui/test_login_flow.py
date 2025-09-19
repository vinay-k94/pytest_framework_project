from framework.ui.pages.login_page import LoginPage

def test_login_flow(driver, base_url):
    page = LoginPage(driver, base_url)
    # NOTE: This is an example; without a running UI and credentials this will fail.
    page.login("admin@example.com", "password123")
    # Add assertions for successful login, e.g., presence of dashboard element.
