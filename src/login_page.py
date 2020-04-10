from base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class LoginPage(BasePage):
    body = (By.CSS_SELECTOR, 'body')
    failure_message = (By.ID, 'loginErrorMessage')
    username_input = (By.ID, 'signInFormUsername')
    password_input = (By.ID, 'signInFormPassword')

    def login(self, username, password):
        self.wait_to_be_redirected(self.base_url)
        self.insert_username(username)
        self.insert_password(password)
        self.submit_login()

    def insert_username(self, username):
        self.wait_for_element(self.username_input)
        field = self.element(self.username_input)
        field.clear()
        field.send_keys(username)

    def insert_password(self, password):
        self.wait_for_element(self.password_input)
        field = self.element(self.password_input)
        field.clear()
        field.send_keys(password)

    def submit_login(self):
        self.wait_for_element(self.username_input)
        field = self.element(self.username_input)
        field.send_keys(Keys.RETURN)

    def get_failure_message_text(self):
        self.wait_for_element(self.failure_message)
        return self.element(self.failure_message).text

    def verify_credentials_invalid(self):
        text = self.get_failure_message_text()
        return text == 'The username or password you entered is invalid'
