import allure
import time
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By  
from locators import ConstructorPageLocators  

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Перейти на страницу по URL")
    def navigate_to(self, url: str) -> None:
        self.driver.get(url)

    _EC_MAP = {
        "presence": EC.presence_of_element_located,
        "visible": EC.visibility_of_element_located,
        "clickable": EC.element_to_be_clickable,
    }

    def _wait_for_element(self, locator, timeout=10, condition="presence"):
        ec_func = self._EC_MAP.get(condition)
        if not ec_func:
            raise ValueError(f"Неизвестное условие ожидания: {condition}")
        wait = WebDriverWait(self.driver, timeout, poll_frequency=0.5)
        return wait.until(ec_func(locator))

    def find_element(self, locator, timeout=10):
        return self._wait_for_element(locator, timeout, "presence")

    def find_visible_element(self, locator, timeout=10):
        return self._wait_for_element(locator, timeout, "visible")

    def find_clickable_element(self, locator, timeout=10):
        return self._wait_for_element(locator, timeout, "clickable")

    @allure.step("Клик по элементу")
    def safe_click(self, locator):
        by, value = locator

        # Сначала убеждаемся, что модальное окно исчезло
        try:
            self.wait.until(EC.invisibility_of_element_located(ConstructorPageLocators.MODAL_OVERLAY))
        except Exception:
            # Если оверлея нет — это нормально, продолжаем
            pass

        element = self.find_clickable_element(locator)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввести текст в поле")
    def fill_field(self, locator, text: str):
        element = self.find_visible_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента")
    def get_text(self, locator):
        return self.find_visible_element(locator).text

    @allure.step("Проверить видимость элемента")
    def is_visible(self, locator) -> bool:
        try:
            elem = self.find_visible_element(locator, timeout=3)
            return elem.is_displayed()
        except TimeoutException:
            return False

    @allure.step("Ждать, пока URL содержит подстроку")
    def wait_for_url_contains(self, substring: str, timeout=15):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(substring))

    @allure.step("Ждать исчезновения элемента")
    def wait_until_hidden(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    @allure.step("Ждать выполнения условия (универсальный метод)")
    def wait_until(self, condition_func, timeout=60):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            result = condition_func(self.driver)
            if result:
                return result
            time.sleep(0.5)
        raise TimeoutException(f"Условие не выполнено за {timeout} сек")