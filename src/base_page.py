import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement


'''
base page class that is inherited by all pages and includes
things available to all pages
'''
class BasePage():
    TIMEOUT = {
        's': 1,
        'm': 3,
        'l': 10,
        'xl': 12
    }

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def goto(self, url):
        ''' wrapper for get() '''
        url = self.base_url + url
        self.driver.get(url)
        return url

    def goto_base_url(self):
        self.driver.get(self.base_url)
        return self.base_url

    def get_base_url(self):
        return self.base_url

    def wait_to_be_redirected(self, current_url):
        return WebDriverWait(self.driver, self.TIMEOUT['l']).until(
            lambda driver: driver.current_url != current_url
        )

    def element(self, locator):
        """wait and get a single element via css selector (eg. #id)."""
        return WebDriverWait(self.driver, self.TIMEOUT['l']).until(
            lambda x: x.find_element(*locator)
        )

    def elements(self, locator):
        ''' wait and get multiple elements via css selector (eg. .class) '''
        return WebDriverWait(self.driver, self.TIMEOUT['l']).until(
            lambda x: x.find_elements(*locator)
        )

    def wait_for_element(self, locator):
        return WebDriverWait(self.driver, self.TIMEOUT['l']).until(
            lambda x: x.find_element(*locator)
        )

    def wait_for_element_to_be_clickable(self, locator):
        return WebDriverWait(self.driver, self.TIMEOUT['l']).until(
            expected_conditions.element_to_be_clickable(locator)
        )

    def click_with_js(self, locator):
        element = None
        if isinstance(locator, str):
            element = self.find_element(locator)
        elif isinstance(locator, WebElement):
            element = locator

        if element is not None:
            self.driver.execute_script("arguments[0].click();", element)
        else:
            raise Exception("Could not click on locator " + element)

    def mock_scroll(self):
        return self.driver.execute_script("window.scrollBy(0,250)")

    def wait_for_element_to_be_visible(self, locator):
        return WebDriverWait(self.driver, self.TIMEOUT['l']).until(
            expected_conditions.visibility_of_element_located(locator)
        )

    def sleep(self, seconds=1):
        ''' sleeps are an abomination... but... '''
        time.sleep(seconds)

    def element_exists(self, element_css):
        ''' test if an element exists '''
        try:
            self.element(element_css)
        except NoSuchElementException:
            return False
        return True

    def switch_to_new_window(self):
        # this keeps chrome from hanging when switching windows... sadness
        self.sleep(1)
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

    def switch_to_first_window(self):
        windows = self.driver.window_handles
        # close current window
        self.driver.close()
        self.driver.switch_to.window(windows[0])
