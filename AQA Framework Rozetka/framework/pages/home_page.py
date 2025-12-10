from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url)

    def search(self, query: str):
        # Перевір локатор пошуку через DevTools
        search_input = self.type(By.NAME, "search", query)
        search_input.submit()

    def open_category(self, category_text: str):
        # Верхнє меню категорій за текстом
        xpath = f"//a[contains(@class,'menu-categories__link') and contains(., '{category_text}')]"
        self.click(By.XPATH, xpath)

    def change_language(self, lang_code: str):
        # Тут простий варіант: переключення за посиланням у футері/шапці
        # Ти можеш підлаштувати локатор під свій інтерфейс Rozetka
        if lang_code == "ru":
            xpath = "//a[contains(@href, 'lang=ru')]"
        else:
            xpath = "//a[contains(@href, 'lang=ua') or contains(@href, 'lang=uk')]"
        self.click(By.XPATH, xpath)
