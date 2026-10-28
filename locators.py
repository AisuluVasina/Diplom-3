from selenium.webdriver.common.by import By

class MainPageLocators:
    """Локаторы главной страницы и хедера"""
    BTN_CONSTRUCTOR = (By.CSS_SELECTOR, 'a[href="/"]')
    BTN_FEED = (By.CSS_SELECTOR, 'a[href="/feed"]')
    BTN_PERSONAL_ACCOUNT = (By.CSS_SELECTOR, 'a[href="/account"]')
    
    # Логотип 
    LOGO = (By.CSS_SELECTOR, 'div[class*="AppHeader_header__logo"]')
    
    # Кнопка "Войти в аккаунт" на главной
    BTN_LOGIN_MAIN = (By.XPATH, './/button[text() = "Войти в аккаунт"]')


class LoginPageLocators:
    """Локаторы страницы входа"""
    INPUT_EMAIL = (By.XPATH, './/label[text()="Email"]/following-sibling::input')
    INPUT_PASSWORD = (By.XPATH, './/input[@name="Пароль"]')
    BTN_SUBMIT = (By.XPATH, './/button[text()="Войти"]')
    
    # Сообщение об ошибке
    ERROR_MSG = (By.XPATH, '//p[text() = "Некорректный пароль"]')
    OVERLAY_LOGIN = (By.CSS_SELECTOR, ".Modal_modal_overlay__x2ZCr")    

class ConstructorPageLocators:
    """Локаторы конструктора бургеров"""
    # Вкладки ингредиентов 
    BUNS_TAB = (By.XPATH, '//span[normalize-space()="Булки"]/..')
    SAUCES_TAB = (By.XPATH, '//span[normalize-space()="Соусы"]/..')
    TOPPINGS_TAB = (By.XPATH, '//span[normalize-space()="Начинки"]/..')

    # Ингредиенты 
    INGREDIENT_BUN = (By.XPATH, "//a[.//img[@alt='Флюоресцентная булка R2-D3']]") 
    INGREDIENT_SAUCE_SPICY = (By.XPATH, "//a[.//img[@alt='Соус Spicy-X']]")

    # Заголовок "Соберите бургер"
    TITLE_ASSEMBLE_THE_BURGER = (By.XPATH, ".//h1[contains(text(), 'Соберите бургер')]")

    # Корзина
    BASKET_COUNTER = (By.CSS_SELECTOR, "p.counter_counter_num")
    BASKET_LIST = (By.CSS_SELECTOR, 'ul[class*="BurgerConstructor_basket__list"]')
    
    # Кнопка заказа
    BTN_CREATE_ORDER = (By.XPATH, "//button[text()='Оформить заказ']")

    BUN_COUNTER_VALUE = (By.XPATH, "//a[.//img[@alt='Флюоресцентная булка R2-D3']]//*[contains(@class, 'counter')]")
    # Модальное окно 
    MODAL_OVERLAY = (By.CSS_SELECTOR, ".Modal_modal_overlay__x2ZCr")
    MODAL_CLOSE_BTN = (By.XPATH, ".//button[contains(@class, 'Modal_modal__close')]")
    MODAL_CLOSE_BTN_SVG = (By.XPATH,".//button[contains(@class, 'Modal_modal__close')]//*[name()='svg']")

    # Элементы внутри модального окна
    MODAL_TITLE = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title')]")
    MODAL_INGREDIENT_NAME = (By.CSS_SELECTOR, 'p[class*="text_type_main-medium"]')
    MODAL_ORDER_NUMBER = (By.CSS_SELECTOR, 'h2[class*="text_type_digits-large"]')

    CONSTRUCTOR_AREA = (By.XPATH, "//span[contains(normalize-space(.), 'Перетяните булочку сюда (верх)')]/ancestor::li")
class OrderFeedPageLocators:
    """Локаторы ленты заказов"""
    HEADER_FEED_OF_ORDERS = (By.XPATH, "//h1[text()='Лента заказов']")
    
    # 1. Локатор для "Выполнено за все время"
    COUNTER_TOTAL = (By.XPATH, "//div[contains(., 'Выполнено за все время')]/p[contains(@class, 'OrderFeed_number')]")

    # 2. Локатор для "Выполнено за сегодня"
    COUNTER_TODAY = (By.XPATH, "//div[contains(., 'Выполнено за сегодня')]/p[contains(@class, 'OrderFeed_number')]")

    # Секция "В работе"
    SECTION_IN_PROGRESS = (By.XPATH, "//h2[text()='В работе']/following-sibling::div")
    
    # Отдельный заказ в ленте
    ORDER_ITEM = (By.CSS_SELECTOR, 'li[class*="OrderHistory_listItem"]')


class PersonalAccountPageLocators:
    """Локаторы личного кабинета"""
    LOGIN_TITLE = (By.XPATH, '//h2[text()="Вход"]')
    FIELDS_NAME = (By.XPATH, '//label[text()="Имя"]/following-sibling::input')
    
    # Кнопка выхода
    BTN_LOGOUT = (By.XPATH, ".//button[text()='Выход']")
    
    # Ссылка регистрации (если нужна)
    BTN_REGISTER = (By.XPATH, '//a[text() = "Зарегистрироваться"]')