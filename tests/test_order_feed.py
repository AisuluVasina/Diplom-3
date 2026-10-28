import allure

from pages.feed_page import FeedPage
from pages.main_page import MainPage

@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Счётчик «Выполнено за всё время» увеличивается после создания заказа")
    @allure.story("Счётчики заказов")
    def test_total_counter_increases_after_order_created(self, driver, logged_in_user):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        with allure.step("Открываем ленту заказов"):
            feed_page.open_feed_page()

        with allure.step("Получаем значение счётчика «Выполнено за всё время» до создания заказа"):
            total_counter_before = feed_page.get_total_counter_value()

        with allure.step("Открываем главную страницу"):
            main_page.open_main_page()

        with allure.step("Создаём заказ"):
            main_page.create_order()

        with allure.step("Закрываем модальное окно заказа"):
            main_page.close_order_modal()

        with allure.step("Открываем ленту заказов после создания заказа"):
            feed_page.open_feed_page()

        with allure.step("Ждём увеличения счётчика «Выполнено за всё время» после создания заказа"):
            total_counter_after = feed_page.wait_until_total_counter_increased(total_counter_before)

        with allure.step("Проверяем, что счётчик «Выполнено за всё время» увеличился"):
            assert total_counter_after > total_counter_before

    @allure.title("Счётчик «Выполнено за сегодня» увеличивается после создания заказа")
    @allure.story("Счётчики заказов")
    def test_today_counter_increases_after_order_created(self, driver, logged_in_user):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        with allure.step("Открываем ленту заказов"):
            feed_page.open_feed_page()

        with allure.step("Получаем значение счётчика «Выполнено за сегодня» до создания заказа"):
            today_counter_before = feed_page.get_today_counter_value()

        with allure.step("Открываем главную страницу"):
            main_page.open_main_page()

        with allure.step("Создаём заказ"):
            main_page.create_order()

        with allure.step("Закрываем модальное окно заказа"):
            main_page.close_order_modal()

        with allure.step("Открываем ленту заказов после создания заказа"):
            feed_page.open_feed_page()

        with allure.step("Ждём увеличения счётчика «Выполнено за сегодня» после создания заказа"):
            today_counter_after = feed_page.wait_until_today_counter_increased(today_counter_before)

        with allure.step("Проверяем, что счётчик «Выполнено за сегодня» увеличился"):
            assert today_counter_after > today_counter_before

    @allure.title("Номер созданного заказа появляется в разделе «В работе»")
    @allure.story("Заказы в работе")
    def test_created_order_number_appears_in_progress_section(self, driver, logged_in_user):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        with allure.step("Открываем главную страницу"):
            main_page.open_main_page()

        with allure.step("Создаём заказ"):
            main_page.create_order()

        with allure.step("Получаем номер заказа из модального окна"):
            order_number = main_page.get_order_number_from_modal()

        with allure.step("Закрываем модальное окно заказа"):
            main_page.close_order_modal()

        with allure.step("Открываем ленту заказов"):
            feed_page.open_feed_page()

        with allure.step("Проверяем, что номер заказа отображается в разделе «В работе»"):
            assert feed_page.is_order_number_in_progress(order_number)