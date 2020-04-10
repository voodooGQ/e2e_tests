from base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class HomePage(BasePage):
    app_logo = (By.CSS_SELECTOR, '.App-logo')

    def signout(self):
        self.goto('/signout')

    def verify_app_logo_visible(self):
        self.wait_for_element(self.app_logo)
        return self.element_exists(self.app_logo)
