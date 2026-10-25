import allure
import pytest
from config import MAIN_URL, LOGIN_URL
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from locators import MainPageLocators, ConstructorPageLocators
# УДАЛИТЬ: from conftest import close_modal_if_present, safe_click
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Основная функциональность")
class TestMainFunctionality:

    @allure.story("Навигация")
    @allure.title("Переход по клику на «Конструктор»")
    def test_navigate_to_constructor(self, driver):
        driver.get(MAIN_URL)
        
        page = ConstructorPage(driver)

        with allure.step("Нажимаем кнопку «Конструктор» в шапке"):
            page.safe_click(MainPageLocators.BTN_CONSTRUCTOR)

        with allure.step("Проверяем, что страница прокрутилась к секции конструктора"):
            assert page.is_visible(ConstructorPageLocators.TITLE_ASSEMBLE_THE_BURGER)

    @allure.story("Навигация")
    @allure.title("Переход по клику на раздел «Лента заказов» (без авторизации)")
    def test_navigate_to_feed_unauthorized(self, driver):
        driver.get(MAIN_URL)
        wait = WebDriverWait(driver, 10)

        with allure.step("Нажимаем кнопку «Лента заказов»"):
            page = ConstructorPage(driver)
            page.safe_click(MainPageLocators.BTN_FEED)

        with allure.step("Проверяем URL — должен содержать /feed"):
            assert "feed" in driver.current_url

    @allure.story("Взаимодействие с ингредиентами")
    @allure.title("Если кликнуть на ингредиент, появится всплывающее окно с деталями")
    def test_modal_window_open(self, driver):
        driver.get(MAIN_URL)
        
        page = ConstructorPage(driver)

        with allure.step("Клик по ингредиенту"):
            page.click_ingredient()

        with allure.step("Проверяем, что модальное окно открылось"):
            assert page.is_modal_open(), "Модальное окно не открылось"

    @allure.story("Взаимодействие с ингредиентами")
    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_modal_window_close(self, driver):
        driver.get(MAIN_URL)
        
        page = ConstructorPage(driver)

        with allure.step("Открываем модальное окно"):
            page.click_ingredient()
            assert page.is_modal_open(), "Модальное окно не открылось для теста закрытия"

        with allure.step("Закрываем модалку через метод страницы"):
            page.close_modal()

        with allure.step("Проверяем, что модальное окно закрыто"):
            assert not page.is_modal_open(), "Модальное окно осталось открытым"

    @allure.story("Корзина и заказы")
    @allure.title("При добавлении ингредиента в заказ счётчик увеличивается")
    def test_ingredient_counter_increase(self, driver, registered_user):
        email, password = registered_user
        driver.get(LOGIN_URL)

        page = ConstructorPage(driver)
        login_page = LoginPage(driver)

        # 1. Авторизация
        with allure.step("Выполняем вход пользователя"):
            login_page.login(email, password)

        # 2. Ждём появления конструктора
        with allure.step("Ждём появления заголовка «Соберите бургер»"):
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(ConstructorPageLocators.TITLE_ASSEMBLE_THE_BURGER),
                message="Не удалось дождаться появления конструктора бургера"
            )

        # 3. Получаем начальное значение счётчика
        with allure.step("Получаем начальное значение счётчика"):
            start_val = page.get_counter_value()
            assert start_val is not None

        # 4. Добавляем ингредиент
        with allure.step("Перетаскиваем булку в зону сборки"):
            page.drag_and_drop_ingredient()

        # 5. Проверяем увеличение счётчика
        with allure.step("Ожидаем увеличения счётчика"):
            def counter_increased(driver):
                current = page.get_counter_value()
                return current is not None and current > start_val

            end_val = WebDriverWait(driver, 10).until(counter_increased,
                message=f"Счётчик не увеличился за 10 секунд")

        assert end_val > start_val