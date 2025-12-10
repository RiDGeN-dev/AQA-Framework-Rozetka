from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    def open(self):
        # Іконка кошика у шапці
        self.click(By.CSS_SELECTOR, "button.header-actions__button_type_cart,"
                                    "a.header-actions__button_type_cart")

    def get_items_titles(self):
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, "a.cart-product__title"
        )
        return [el.text for el in elements]
