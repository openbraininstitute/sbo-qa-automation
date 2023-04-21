import os
import logging
import pytest

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.fixture(scope="class")
def setup(request):

    # Initialize webdriver object
    browser = webdriver.Chrome()

    # Setting explicit wait
    wait = WebDriverWait(browser, 10)
    request.cls.browser = browser
    request.cls.wait = wait
    yield browser, wait

    browser.quit()


@pytest.fixture(scope="module")
def logger():

    # Initializing the logger object
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter("%(levelname)s : %(asctime)s : %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(filename='test.log')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(levelname)s : %(asctime)s : %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


@pytest.fixture(scope="function")
def navigate_to_login(setup):
    browser, wait = setup
    home_page = HomePage(browser, wait)
    home_page.go_to_home_page()
    login_button = home_page.find_login_button()
    assert login_button.is_displayed()
    login_button.click()
    wait.until(EC.url_contains("auth"))
    login_url = browser.current_url
    yield login_url


@pytest.fixture(scope="function")
def login(setup, navigate_to_login):
    login_page = LoginPage(*setup)
    login_page.go_to_login_page(navigate_to_login)
    yield login_page

