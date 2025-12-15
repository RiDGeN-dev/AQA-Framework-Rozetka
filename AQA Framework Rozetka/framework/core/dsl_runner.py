import shlex
from pathlib import Path

from .context import create_context


class DslRunner:
    """
    Інтерпретатор нашого DSL.
    Читає .bdd-файл пострічково, виконує команди типу:
    OPEN_HOME
    SEARCH "iphone 15"
    SORT_BY_PRICE "asc"
    ASSERT_PRICES_SORTED "asc"
    """

    def __init__(self, dsl_path: Path):
        self.dsl_path = dsl_path
        self.context = create_context()

        # Мапа команд DSL -> методи
        self.commands = {
            "OPEN_HOME": self.cmd_open_home,
            "SEARCH": self.cmd_search,
            "SORT_BY_PRICE": self.cmd_sort_by_price,
            "OPEN_CATEGORY": self.cmd_open_category,
            "CHANGE_LANGUAGE": self.cmd_change_language,
            "OPEN_FIRST_PRODUCT": self.cmd_open_first_product,
            "ADD_TO_CART": self.cmd_add_to_cart,
            "OPEN_CART": self.cmd_open_cart,
            "ASSERT_RESULTS_CONTAIN": self.cmd_assert_results_contain,
            "ASSERT_PRICES_SORTED": self.cmd_assert_prices_sorted,
            "ASSERT_CATEGORY_PAGE_TITLE_CONTAINS": self.cmd_assert_category_title_contains,
            "ASSERT_LANGUAGE_IS": self.cmd_assert_language_is,
            "ASSERT_CART_CONTAINS": self.cmd_assert_cart_contains,
        }

    # ==== основний інтерфейс ====

    def run(self):
        """
        Запускає сценарій з .bdd файлу.
        """
        try:
            with self.dsl_path.open(encoding="utf-8") as f:
                for raw_line in f:
                    line = raw_line.strip()
                    # Пропускаємо службові рядки
                    if (
                        not line
                        or line.startswith("#")
                        or line.startswith("Feature")
                        or line.startswith("Scenario")
                    ):
                        continue
                    self._execute_line(line)
        finally:
            self.context.driver.quit()

    def _execute_line(self, line: str):
        """
        Парсинг і виконання одного рядка DSL.
        Використовуємо shlex, щоб коректно працювали лапки.
        """
        print(f"[DSL] Executing: {line}")  # щоб тобі видно було кроки в консолі

        parts = shlex.split(line)
        cmd = parts[0]
        args = parts[1:]

        handler = self.commands.get(cmd)
        if not handler:
            raise ValueError(f"Unknown DSL command: {cmd}")

        handler(*args)

    # ==== Команди ====

    def cmd_open_home(self):
        self.context.home_page.open()

    def cmd_search(self, query: str):
        self.context.home_page.search(query)

    def cmd_sort_by_price(self, order: str):
        self.context.search_results_page.sort_by_price(order)

    def cmd_open_category(self, category_name: str):
        self.context.home_page.open_category(category_name)

    def cmd_change_language(self, lang_code: str):
        """
        Тут ти вже сам підженеш під Rozetka — наприклад, UA / EN.
        Я не чіпаю ніякі інші мови.
        """
        self.context.home_page.change_language(lang_code)

    def cmd_open_first_product(self):
        """
        Відкриваємо перший товар з результатів пошуку.
        """
        titles = self.context.search_results_page.get_product_titles()
        if not titles:
            raise AssertionError("No products found to open")

        from selenium.webdriver.common.by import By

        first_tile = self.context.driver.find_element(
            By.CSS_SELECTOR, "div.goods-tile a.goods-tile__picture"
        )
        first_tile.click()

    def cmd_add_to_cart(self):
        self.context.product_page.add_to_cart()

    def cmd_open_cart(self):
        self.context.cart_page.open()

    # ==== Асерти ====

    def cmd_assert_results_contain(self, text: str):
        titles = self.context.search_results_page.get_product_titles()
        if not any(text.lower() in t.lower() for t in titles):
            raise AssertionError(
                f"'{text}' not found in any product title: {titles}"
            )

    def cmd_assert_prices_sorted(self, order: str):
        prices = self.context.search_results_page.get_prices()
        sorted_prices = sorted(prices)
        if order == "desc":
            sorted_prices = list(reversed(sorted_prices))

        if prices != sorted_prices:
            raise AssertionError(
                f"Prices not sorted {order}: {prices}"
            )

    def cmd_assert_category_title_contains(self, text: str):
        title = self.context.category_page.get_title()
        if text.lower() not in title.lower():
            raise AssertionError(
                f"'{text}' not in category title '{title}'"
            )

    def cmd_assert_language_is(self, lang_code: str):
        """
        Дуже простий варіант: перевірка наявності коду мови в URL
        (ти можеш потім зробити розумніше).
        """
        current_url = self.context.driver.current_url
        if lang_code.lower() not in current_url.lower():
            raise AssertionError(
                f"Language '{lang_code}' is not reflected in url: {current_url}"
            )

    def cmd_assert_cart_contains(self, text: str):
        titles = self.context.cart_page.get_items_titles()
        if not any(text.lower() in t.lower() for t in titles):
            raise AssertionError(
                f"'{text}' not found in cart items: {titles}"
            )
