from selenium.webdriver.common.by import By
from framework.ui.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self, username: str, password: str):
        self.open("/login")
        self.find(*self.USERNAME).send_keys(username)
        self.find(*self.PASSWORD).send_keys(password)
        self.find(*self.SUBMIT).click()
