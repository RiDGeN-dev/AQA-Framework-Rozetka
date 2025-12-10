from dataclasses import dataclass

from .driver_manager import create_driver
from framework.pages.home_page import HomePage
from framework.pages.search_results_page import SearchResultsPage
from framework.pages.category_page import CategoryPage
from framework.pages.product_page import ProductPage
from framework.pages.cart_page import CartPage


@dataclass
class TestContext:
    driver: object
    home_page: HomePage
    search_results_page: SearchResultsPage
    category_page: CategoryPage
    product_page: ProductPage
    cart_page: CartPage


def create_context() -> TestContext:
    driver = create_driver()
    base_url = "https://rozetka.com.ua/"
    return TestContext(
        driver=driver,
        home_page=HomePage(driver, base_url),
        search_results_page=SearchResultsPage(driver),
        category_page=CategoryPage(driver),
        product_page=ProductPage(driver),
        cart_page=CartPage(driver),
    )
