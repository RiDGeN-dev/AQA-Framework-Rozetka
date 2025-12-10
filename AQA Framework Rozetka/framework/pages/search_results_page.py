from selenium.webdriver.common.by import By
from .base_page import BasePage


class SearchResultsPage(BasePage):
    def get_product_titles(self):
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, "span.goods-tile__title"
        )
        return [el.text for el in elements]

    def sort_by_price(self, order: str):
        # Дуже спрощено: знаходимо селект сортування
        self.click(By.CSS_SELECTOR, "select[formcontrolname='sort']")
        if order == "asc":
            option_value = "price"
        else:
            option_value = "price_desc"
        self.click(By.CSS_SELECTOR, f"option[value='{option_value}']")

    def get_prices(self):
        price_elements = self.driver.find_elements(
            By.CSS_SELECTOR, "span.goods-tile__price-value"
        )
        prices = []
        for el in price_elements:
            text = el.text.replace(" ", "").replace("₴", "")
            try:
                prices.append(int(text))
            except ValueError:
                continue
        return prices
