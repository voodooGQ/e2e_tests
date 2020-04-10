"""Test deploying a base line static site."""
import logging
from login_page import LoginPage
from home_page import HomePage

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import boto3


LOGGER = logging.getLogger(__name__)


class Test(object):
    login_page = None
    home_page = None
    driver = None

    def run(self):
        try:
            distribution_domain = 'd1w6fvriuwai1z.cloudfront.net'
            self.driver = webdriver.Chrome()
            self.driver.set_window_size(1200, 800)
            self.login_page = LoginPage(self.driver, 'https://%s' % distribution_domain)
            self.home_page = HomePage(self.driver, 'https://%s' % distribution_domain)
            self.login_page.mock_scroll();
            self.test_for_invalid_credentials()
            self.test_for_successful_login()
            self.test_for_successful_signout()
            self.driver.quit()
        except AssertionError:
            print('Tests Failed')
            self.driver.quit()
        else:
            print('Tests Passed')

    def test_for_invalid_credentials(self):
        self.login_page.goto_base_url()
        self.login_page.login('foo', 'bar')
        assert self.login_page.verify_credentials_invalid()

    def test_for_successful_login(self):
        self.login_page.goto_base_url()
        self.login_page.login('shane.smith@rackspace.com', 'P@ssw0rd')
        assert self.home_page.verify_app_logo_visible()

    def test_for_successful_signout(self):
        self.home_page.signout()
        # Go to a different page so we don't get the home cache
        self.login_page.goto('/foo')
        self.login_page.element_exists(self.login_page.username_input)


Test().run()
