import allure
from pages.base_page import BasePage
from locators import OrderFeedPageLocators
from config import FEED_URL
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class FeedPage(BasePage):
    @allure.step("Открыть ленту заказов")
    def open_feed_page(self):
        self.navigate_to(FEED_URL)

    @allure.step("Получить значение счётчика «Выполнено за всё время»")
    def get_total_counter_value(self):
        text = self.get_text(OrderFeedPageLocators.COUNTER_TOTAL)
        return int(text.replace(" ", ""))

    @allure.step("Получить значение счётчика «Выполнено за сегодня»")
    def get_today_counter_value(self):
        text = self.get_text(OrderFeedPageLocators.COUNTER_TODAY)
        return int(text.replace(" ", ""))

    @allure.step("Ждать увеличения счётчика «Выполнено за всё время»")
    def wait_until_total_counter_increased(self, old_value: int):
        def condition(driver):
            new_val = self.get_total_counter_value()
            if new_val > old_value:
                return new_val
            return False
        return self.wait_until(condition, timeout=60)

    @allure.step("Ждать увеличения счётчика «Выполнено за сегодня»")
    def wait_until_today_counter_increased(self, old_value: int):
        def condition(driver):
            new_val = self.get_today_counter_value()
            if new_val > old_value:
                return new_val
            return False
        return self.wait_until(condition, timeout=60)

    @allure.step("Проверить, что номер заказа виден в разделе «В работе»")
    def is_order_number_in_progress(self, order_number: str) -> bool:
        """
        Проверяет, что номер заказа отображается в разделе «В работе».
        """
        # Локатор на карточку заказа (ORDER_ITEM)
        locator = OrderFeedPageLocators.ORDER_ITEM

        try:
            # Ждём появления хотя бы одной карточки заказа
            self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return False

        # Получаем все карточки заказов
        order_items = self.driver.find_elements(*locator)

        # Ищем номер заказа в тексте карточек
        for item in order_items:
            if order_number in item.text:
                return True

        return False