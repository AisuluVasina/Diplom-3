import pytest
import requests
from config import BASE_URL
from pages.login_page import LoginPage
from locators import ConstructorPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from helpers import generate_email, generate_password
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    if browser == "chrome":
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        options = ChromeOptions()
        driver = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.set_preference("browser.startup.page", 0)
        options.set_preference("browser.startup.homepage", "")
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(60)

    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()

@pytest.fixture
def registered_user(driver):
    """
    Создает пользователя через API.
    ВАЖНО: Не использует assert внутри фикстуры. Если регистрация не удалась, 
    фикстура упадет с ошибкой запроса, что будет понятнее в отчете.
    """
    email = generate_email()
    password = generate_password()
    name = "Tester"

    payload = {"email": email, "password": password, "name": name}
    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
    
    # Если статус не 200, фикстура упадет здесь, а не внутри теста
    if response.status_code != 200:
        pytest.fail(f"Регистрация не удалась: {response.text}")

    yield email, password

    # Очистка данных после теста
    try:
        login_payload = {"email": email, "password": password}
        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json=login_payload)
        
        if login_resp.status_code == 200:
            token = login_resp.json().get("accessToken")
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                requests.delete(f"{BASE_URL}/api/auth/user", headers=headers)
    except Exception:
        pass

@pytest.fixture
def logged_in_user(driver, registered_user):
    email, password = registered_user
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(email, password)
    
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located(ConstructorPageLocators.TITLE_ASSEMBLE_THE_BURGER))

    return driver