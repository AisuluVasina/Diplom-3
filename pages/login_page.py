import allure

from pages.base_page import BasePage
from locators import LoginPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    @allure.step("Открыть страницу входа")
    def open(self):
        from config import LOGIN_URL
        self.navigate_to(LOGIN_URL)

    @allure.step("Ввести email")
    def set_email(self, email: str):
        self.fill_field(LoginPageLocators.INPUT_EMAIL, email)

    @allure.step("Ввести пароль")
    def set_password(self, password: str):
        self.fill_field(LoginPageLocators.INPUT_PASSWORD, password)

    @allure.step("Нажать кнопку Войти")
    def submit_login(self):
        self.safe_click(LoginPageLocators.BTN_SUBMIT)

    @allure.step("Выполнить вход")
    def login(self, email: str, password: str):
        self.set_email(email)
        self.set_password(password)
        self.submit_login()

    def is_authorized(self) -> bool:
        return self.is_element_visible(*LoginPageLocators.PROFILE_ICON)