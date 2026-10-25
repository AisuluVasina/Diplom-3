import allure 
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from locators import ConstructorPageLocators
import time
import re

class ConstructorPage(BasePage):
    
    def click_ingredient(self):
        """Клик по ингредиенту."""
        self.ensure_no_modal()
        try:
            ingredient = self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.INGREDIENT_BUN))
            ingredient.click()
            print("[DEBUG] Клик по ингредиенту выполнен.")
        except ElementClickInterceptedException:
            print("[DEBUG] Клик перехвачен! Закрываем модалку и пробуем снова.")
            self.close_modal()
            ingredient = self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.INGREDIENT_BUN))
            ingredient.click()

    def is_modal_open(self):
        """Проверяет наличие оверлея."""
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(ConstructorPageLocators.MODAL_OVERLAY)
            )
            return True
        except TimeoutException:
            return False

    def close_modal(self):
        """Закрывает модалку максимально надежно."""
        print("[DEBUG] Попытка закрыть модалку...")
        
        locator = ConstructorPageLocators.MODAL_CLOSE_BTN
        
        try:
            # 1. Ждем видимости кнопки
            close_btn = self.wait.until(EC.visibility_of_element_located(locator))
            
            # 2. Пытаемся кликнуть обычным способом
            close_btn.click()
            print("[DEBUG] Обычный клик успешен.")
            
        except Exception as e:
            print(f"[DEBUG] Обычный клик не прошел ({e}). Пробуем JS-клик...")
            try:
                close_btn = self.find_element(locator)
                self.driver.execute_script("arguments.click();", close_btn)
                print("[DEBUG] JS-клик успешен.")
            except Exception as js_err:
                print(f"[DEBUG] Не удалось закрыть модалку: {js_err}")
                raise

        # 4. Ждем исчезновения оверлея (подтверждение закрытия)
        print("[DEBUG] Ждем исчезновения оверлея...")
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(ConstructorPageLocators.MODAL_OVERLAY)
        )
        print("[DEBUG] Оверлей исчез. Модалка закрыта.")

    def ensure_no_modal(self):
        """Гарантирует отсутствие модального окна."""
        if self.is_modal_open():
            self.close_modal()
            #time.sleep(0.5)

    def get_counter_value(self):
        """Возвращает числовое значение счётчика булки. Если не найдено - возвращает None."""
        try:
            counter_element = self.find_element(ConstructorPageLocators.BUN_COUNTER_VALUE)
            text = counter_element.text.strip()
            
            if text.isdigit():
                return int(text)
            else:
                # Если там текст, пробуем вытащить цифры регуляркой или просто вернуть 0
                import re
                match = re.search(r'\d+', text)
                return int(match.group()) if match else 0
        except Exception:
            return None

    def drag_and_drop_ingredient(self):
        wait = WebDriverWait(self.driver, 15)

        # 1. Находим булку (источник)
        bun_element = wait.until(
            EC.element_to_be_clickable(ConstructorPageLocators.INGREDIENT_BUN),
            message="Не найдена карточка булки для перетаскивания"
        )

        # 2. Находим зону сборки (цель)
        drop_zone = wait.until(
            EC.presence_of_element_located(ConstructorPageLocators.CONSTRUCTOR_AREA),
            message="Не найдена зона сборки (верхняя булка корзины)"
        )

        print("[DEBUG] Элементы найдены. Запускаем JS-эмуляцию Drag-and-Drop...")

        # JS-скрипт: вручную создаёт события dragstart → dragover → drop → dragend
        drag_script = """
            function simulateDrag(source, target) {
                // 1. Начало драга
                var dragStartEvent = new DragEvent('dragstart', { bubbles: true });
                source.dispatchEvent(dragStartEvent);

                // 2. Перемещение над целью (обязательно для React)
                var dragOverEvent = new DragEvent('dragover', { bubbles: true });
                target.dispatchEvent(dragOverEvent);

                // 3. Сброс элемента
                var dropEvent = new DragEvent('drop', { bubbles: true });
                target.dispatchEvent(dropEvent);

                // 4. Конец драга
                var dragEndEvent = new DragEvent('dragend', { bubbles: true });
                source.dispatchEvent(dragEndEvent);
            }
            simulateDrag(arguments[0], arguments[1]);
        """

        # Выполняем JS, передавая элементы напрямую (Selenium сам их «упакует»)
        self.driver.execute_script(drag_script, bun_element, drop_zone)

        # React должен успеть обновить стейт и перерисовать DOM
        print("[DEBUG] JS-драг выполнен. Ждём обновления стейта (2.5 сек)...")
        #time.sleep(2.5)

        self.ensure_no_modal()

    def create_order(self):
        self.click(ConstructorPageLocators.BTN_CREATE_ORDER)
        wait = WebDriverWait(self.driver, 15)
        wait.until(
            EC.visibility_of_element_located(ConstructorPageLocators.MODAL_TITLE),
            message="Модальное окно с номером заказа не открылось"
        )
        order_number_element = self.find_element(ConstructorPageLocators.MODAL_ORDER_NUMBER)
        text = order_number_element.text.strip()
        match = re.search(r'\d+', text)
        assert match, f"Не удалось извлечь номер заказа из текста: {text}"
        return match.group()

    def create_full_order(self) -> str:
        """
        Собирает бургер (минимум 1 ингредиент) и оформляет заказ.
        """
        wait = self.wait

        with allure.step("Добавляем 1 ингредиент (булку) в конструктор"):
            # Гарантируем, что модалка не перекрывает элементы
            self.ensure_no_modal()
            
            # Перетаскиваем булку
            self.drag_and_drop_ingredient()

        with allure.step("Ждём, пока кнопка «Оформить заказ» станет кликабельной"):
            btn = wait.until(
                EC.element_to_be_clickable(ConstructorPageLocators.BTN_CREATE_ORDER),
                message="Кнопка «Оформить заказ» так и не стала кликабельной. "
                        "Возможно, бургер не собран или интерфейс завис."
            )
            btn.click()

        with allure.step("Получаем номер заказа из модального окна"):
            # Сначала убеждаемся, что модальное окно открылось (заголовок виден)
            wait.until(
                EC.visibility_of_element_located(ConstructorPageLocators.MODAL_TITLE),
                message="Модальное окно с номером заказа не открылось после клика."
            )

            order_number_el = wait.until(
                EC.visibility_of_element_located(ConstructorPageLocators.MODAL_ORDER_NUMBER)
            )
            order_text = order_number_el.text.strip()

            import re
            match = re.search(r'\d+', order_text)
            assert match, f"Не удалось извлечь номер заказа из текста: {order_text}"
            return match.group()