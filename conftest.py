import pytest
import requests
import time
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from helpers import generate_email, generate_password
from config import BASE_URL
from locators import ConstructorPageLocators  # <--- ЭТО БЫЛО ПРОПУЩЕНО, из-за чего тесты не работали
from pages.login_page import LoginPage

def safe_click(driver, locator, timeout=10):
    """
    Безопасный клик: ждет, пока элемент станет кликабельным, затем кликает.
    """
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable(locator))
    element.click()


def close_modal_if_present(driver):
    """
    Ждёт исчезновения модального окна. Если его нет — сразу выходит.
    Использует явное ожидание невидимости оверлея.
    """
    wait = WebDriverWait(driver, 15)
    
    # Проверяем, есть ли вообще оверлей (фон затемнения). 
    # Если его нет - модалки нет, выходим сразу.
    try:
        overlay = driver.find_element(*ConstructorPageLocators.MODAL_OVERLAY)
        if overlay.is_displayed():
            print("[DEBUG] Модалка обнаружена, начинаем ...")
            
            # 1. Пытаемся нажать на крестик
            try:
                close_btn = wait.until(
                    EC.element_to_be_clickable(ConstructorPageLocators.MODAL_CLOSE_BTN)
                )
                close_btn.click()
                print("[DEBUG] Кнопка закрытия модалки нажата.")
            except Exception:
                print("[DEBUG] Кнопки закрытия не видно, пробуем ждать исчезновения.")

            # 2. Ждём, пока оверлей реально исчезнет со страницы
            wait.until(
                EC.invisibility_of_element_located(ConstructorPageLocators.MODAL_OVERLAY),
                message="Не удалось закрыть модальное окно за 15 секунд!"
            )
            print("[DEBUG] Оверлей исчез, путь свободен.")
        else:
            print("[DEBUG] Оверлей есть, но не виден. Всё ок.")
            
    except Exception:
        pass


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    if browser == "chrome":
        options = ChromeOptions()
        driver = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.set_preference("browser.startup.page", 0)
        options.set_preference("browser.startup.homepage", "")
        options.set_preference("network.http.connection-timeout", 30)
        options.set_preference("dom.max_script_run_time", 30)
        # ---------------------
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(60)

    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

@pytest.fixture
def registered_user(driver):
    email = generate_email()
    password = generate_password()
    name = "Tester"

    payload = {"email": email, "password": password, "name": name}
    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
    assert response.status_code == 200, f"Регистрация не удалась: {response.text}"

    yield email, password

    # 2. УДАЛЕНИЕ ТОЛЬКО ПОСЛЕ ЗАВЕРШЕНИЯ ТЕСТА
    try:
        # Логинимся, чтобы получить токен для удаления
        login_payload = {"email": email, "password": password}
        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json=login_payload)
        
        if login_resp.status_code == 200:
            token = login_resp.json().get("accessToken")
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                # Удаляем пользователя
                del_resp = requests.delete(f"{BASE_URL}/api/auth/user", headers=headers)
                print(f"[DEBUG] Пользователь {email} удалён. Статус: {del_resp.status_code}")
    except Exception as e:
        print(f"[WARNING] Не удалось удалить пользователя {email}: {e}")

def debug_step(driver, message):
    """
    Делает скриншот для отладки.
    ВНИМАНИЕ: Не используй в продакшн-тестах, так как замедляет их.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debug_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"[DEBUG] {message} -> Скриншот сохранен: {filename}")

@pytest.fixture
def logged_in_user(driver, registered_user):
    email, password = registered_user
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(email, password)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located(ConstructorPageLocators.TITLE_ASSEMBLE_THE_BURGER))

    yield driver