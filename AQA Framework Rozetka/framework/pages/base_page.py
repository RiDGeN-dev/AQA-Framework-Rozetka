from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find(self, by, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def click(self, by, locator, timeout=10):
        el = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
        el.click()
        return el

    def type(self, by, locator, text, timeout=10):
        el = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
        el.clear()
        el.send_keys(text)
        return el
