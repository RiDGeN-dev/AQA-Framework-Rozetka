from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductPage(BasePage):
    def add_to_cart(self):
        self.click(By.CSS_SELECTOR, "button.buy-button, button[aria-label='Купити']")
