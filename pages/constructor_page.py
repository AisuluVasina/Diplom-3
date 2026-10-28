import allure
import re
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from locators import ConstructorPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class ConstructorPage(BasePage):
    
    def click_ingredient(self):
        self.ensure_no_modal()
        ingredient = self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.INGREDIENT_BUN))
        try:
            ingredient.click()
        except ElementClickInterceptedException:
            self.close_modal()
            ingredient = self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.INGREDIENT_BUN))
            ingredient.click()

    def is_modal_open(self):
        """Проверяет наличие оверлея."""
        try:
            self.wait.until(EC.visibility_of_element_located(ConstructorPageLocators.MODAL_OVERLAY))
            return True
        except TimeoutException:
            return False

    def close_modal(self):
        if self.is_modal_open():
            close_btn = self.find_element(ConstructorPageLocators.MODAL_CLOSE_BTN)
            # Сначала пробуем обычный клик
            try:
                close_btn.click()
            except ElementClickInterceptedException:
                # Если не кликается — используем JS
                self.execute_script("arguments[0].click();", close_btn)
            # Ждем исчезновения оверлея
            self.wait_until_hidden(ConstructorPageLocators.MODAL_OVERLAY)

    def ensure_no_modal(self):
        if self.is_modal_open():
            self.close_modal()

    def get_counter_value(self):
        try:
            counter_element = self.find_element(ConstructorPageLocators.BUN_COUNTER_VALUE)
            text = counter_element.text.strip()
            
            if text.isdigit():
                return int(text)
            else:
                match = re.search(r'\d+', text)
                return int(match.group()) if match else 0
        except Exception:
            return None

    def drag_and_drop_ingredient(self):
        self.ensure_no_modal()

        bun_element = self.wait.until(
            EC.element_to_be_clickable(ConstructorPageLocators.INGREDIENT_BUN)
        )
        drop_zone = self.wait.until(
            EC.presence_of_element_located(ConstructorPageLocators.CONSTRUCTOR_AREA)
        )

        html5_drag_script = """
            (function(source, target) {
                var dataTransfer = new DataTransfer();

                var dragStartEvent = new DragEvent('dragstart', { bubbles: true, cancelable: true, view: window, dataTransfer: dataTransfer });
                source.dispatchEvent(dragStartEvent);

                var dragOverEvent = new DragEvent('dragover', { bubbles: true, cancelable: true, view: window, dataTransfer: dataTransfer });
                target.dispatchEvent(dragOverEvent);

                var dropEvent = new DragEvent('drop', { bubbles: true, cancelable: true, view: window, dataTransfer: dataTransfer });
                target.dispatchEvent(dropEvent);

                var dragEndEvent = new DragEvent('dragend', { bubbles: true, cancelable: true, view: window, dataTransfer: dataTransfer });
                source.dispatchEvent(dragEndEvent);
            })(arguments[0], arguments[1]);
        """
        self.execute_script(html5_drag_script, bun_element, drop_zone)
        self.ensure_no_modal()

    def create_order(self):
        self.safe_click(ConstructorPageLocators.BTN_CREATE_ORDER)
        
        self.wait.until(
            EC.visibility_of_element_located(ConstructorPageLocators.MODAL_TITLE),
            message="Модальное окно с номером заказа не открылось"
        )
        
        order_number_element = self.find_element(ConstructorPageLocators.MODAL_ORDER_NUMBER)
        text = order_number_element.text.strip()
        match = re.search(r'\d+', text)
        assert match, f"Не удалось извлечь номер заказа из текста: {text}"
        return match.group()

    def create_full_order(self) -> str:
        with allure.step("Добавляем 1 ингредиент (булку) в конструктор"):
            self.ensure_no_modal()
            self.drag_and_drop_ingredient()

        with allure.step("Ждём, пока кнопка «Оформить заказ» станет кликабельной"):
            btn = self.wait.until(
                EC.element_to_be_clickable(ConstructorPageLocators.BTN_CREATE_ORDER),
                message="Кнопка «Оформить заказ» так и не стала кликабельной."
            )
            btn.click()

        with allure.step("Получаем номер заказа из модального окна"):
            self.wait.until(
                EC.visibility_of_element_located(ConstructorPageLocators.MODAL_TITLE),
                message="Модальное окно с номером заказа не открылось после клика."
            )

            order_number_el = self.wait.until(
                EC.visibility_of_element_located(ConstructorPageLocators.MODAL_ORDER_NUMBER)
            )
            order_text = order_number_el.text.strip()

            match = re.search(r'\d+', order_text)
            assert match, f"Не удалось извлечь номер заказа из текста: {order_text}"
            return match.group()

    def is_constructor_loaded(self):
        return self.is_visible(ConstructorPageLocators.TITLE_ASSEMBLE_THE_BURGER)

    def wait_for_constructor_loaded(self, timeout=15):
        self.wait.until(
            EC.visibility_of_element_located(ConstructorPageLocators.TITLE_ASSEMBLE_THE_BURGER),
            message="Не удалось дождаться появления конструктора бургера"
        )

    def wait_for_counter_increase(self, start_val: int, timeout: int = 15) -> int:
        start_val = int(start_val)

        def counter_increased(driver):
            current = self.get_counter_value()
            if current is None:
                return False
            try:
                current_int = int(current)
            except (ValueError, TypeError):
                return False
            return current_int > start_val
        
        try:
            return self.wait.until(counter_increased, message=f"Счётчик не увеличился за {timeout} сек (было: {start_val})")
        except TimeoutException as e:
            final_val = self.get_counter_value()
            raise TimeoutException(
                f"{str(e)} (фактическое значение в конце ожидания: {final_val})"
            ) from e