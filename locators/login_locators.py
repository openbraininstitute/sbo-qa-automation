from selenium.webdriver.common.by import By


class LoginPageLocators:
    login_btn = (By.XPATH, "//button[contains(text(), 'Login')]")