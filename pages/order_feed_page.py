from pages.base_page import BasePage
from locators import OrderFeedPageLocators

class OrderFeedPage(BasePage):
    def get_total_counter(self):
        return int(self.get_text(OrderFeedPageLocators.COUNTER_TOTAL))

    def get_today_counter(self):
        return int(self.get_text(OrderFeedPageLocators.COUNTER_TODAY))

    def check_order_in_progress(self, order_number):
        progress_text = self.get_text(OrderFeedPageLocators.SECTION_IN_PROGRESS)
        return str(order_number) in progress_text