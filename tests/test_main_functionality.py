import allure
import pytest
from config import MAIN_URL, LOGIN_URL
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from pages.main_page import MainPage

@allure.feature("Основная функциональность")
class TestMainFunctionality:

    @allure.story("Навигация")
    @allure.title("Переход по клику на «Конструктор»")
    def test_navigate_to_constructor(self, driver):
        page = MainPage(driver)
        page.open_main_page()

        with allure.step("Нажимаем кнопку «Конструктор» в шапке"):
            page.click_constructor_btn()

        with allure.step("Проверяем, что видим заголовок «Соберите бургер»"):
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_loaded()

    @allure.story("Навигация")
    @allure.title("Переход по клику на раздел «Лента заказов» (без авторизации)")
    def test_navigate_to_feed_unauthorized(self, driver):
        page = MainPage(driver)
        page.open_main_page()

        with allure.step("Нажимаем кнопку «Лента заказов»"):
            page.go_to_feed()

        with allure.step("Проверяем URL — должен содержать /feed"):
            assert page.is_url_contains("feed")

    @allure.story("Взаимодействие с ингредиентами")
    @allure.title("Если кликнуть на ингредиент, появится всплывающее окно с деталями")
    def test_modal_window_open(self, driver):
        page = MainPage(driver)
        page.open_main_page()

        constructor_page = ConstructorPage(driver)

        with allure.step("Клик по ингредиенту"):
            constructor_page.click_ingredient()

        with allure.step("Проверяем, что модальное окно открылось"):
            assert constructor_page.is_modal_open()

    @allure.story("Взаимодействие с ингредиентами")
    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_modal_window_close(self, driver):
        page = MainPage(driver)
        page.open_main_page()

        constructor_page = ConstructorPage(driver)

        with allure.step("Открываем модальное окно"):
            constructor_page.click_ingredient()

        with allure.step("Закрываем модалку через метод страницы"):
            constructor_page.close_modal()

        with allure.step("Проверяем, что модальное окно закрыто"):
            assert not constructor_page.is_modal_open()

    @allure.story("Корзина и заказы")
    @allure.title("При добавлении ингредиента в заказ счётчик увеличивается")
    def test_ingredient_counter_increase(self, driver, registered_user):
        email, password = registered_user

        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(email, password)

        constructor_page = ConstructorPage(driver)

        with allure.step("Ждём появления заголовка «Соберите бургер» через метод страницы"):
            constructor_page.wait_for_constructor_loaded()

        with allure.step("Получаем начальное значение счётчика"):
            start_val = constructor_page.get_counter_value()
            assert start_val is not None

        with allure.step("Перетаскиваем булку в зону сборки"):
            constructor_page.drag_and_drop_ingredient()

        with allure.step("Ожидаем увеличения счётчика"):
            end_val = constructor_page.wait_for_counter_increase(start_val)

        assert end_val > start_val