from selenium.webdriver.common.by import By
from .base_page import BasePage


class CategoryPage(BasePage):
    def get_title(self):
        # Наприклад заголовок категорії
        return self.find(By.CSS_SELECTOR, "h1.catalog-heading__title").text
