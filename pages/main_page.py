import allure
import re
from pages.base_page import BasePage
from locators import MainPageLocators, ConstructorPageLocators
from config import BASE_URL
from pages.constructor_page import ConstructorPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class MainPage(BasePage):
    @allure.step("Открыть главную страницу")
    def open_main_page(self):
        self.navigate_to(BASE_URL)

    @allure.step("Перейти в Конструктор бургеров")
    def go_to_constructor(self):
        self.safe_click(MainPageLocators.BTN_CONSTRUCTOR)

    @allure.step("Перейти в Ленту заказов")
    def go_to_feed(self):
        self.safe_click(MainPageLocators.BTN_FEED)

    @allure.step("Создать заказ (собрать бургер и нажать Оформить заказ)")
    def create_order(self):
        # 1. Собираем бургер через страницу конструктора
        constructor = ConstructorPage(self.driver)
        constructor.drag_and_drop_ingredient()
        
        # 2. Нажимаем кнопку "Оформить заказ"
        self.safe_click(ConstructorPageLocators.BTN_CREATE_ORDER)

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        self.safe_click(ConstructorPageLocators.MODAL_CLOSE_BTN)

    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self) -> str:
        def number_is_ready(driver):
            title_text = self.get_text(ConstructorPageLocators.MODAL_TITLE)
            match = re.search(r"\d{4,}", title_text)
            if match and match.group() != "9999":
                return match.group()
            return False
        return self.wait_until(number_is_ready, timeout=60)

    def click_constructor_btn(self):
        """Клик по кнопке «Конструктор» в шапке."""
        self.safe_click(MainPageLocators.BTN_CONSTRUCTOR)

    def go_to_feed(self):
        """Клик по кнопке «Лента заказов»."""
        self.safe_click(MainPageLocators.BTN_FEED)

    def is_url_contains(self, substring):
        """Проверка, содержит ли текущий URL подстроку."""
        return substring in self.driver.current_url