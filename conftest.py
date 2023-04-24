import logging
import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.home_page import HomePage
from pages.login_page import LoginPage
from util.util_base import load_config


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
    logger.setLevel(logging.INFO)

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


# This is the initial fixture that works
@pytest.fixture(scope="function")
def login(setup, navigate_to_login):
    login_page = LoginPage(*setup)
    login_page.go_to_login_page(navigate_to_login)
    yield login_page

# Login fixture that is used throughout the project
@pytest.fixture(scope="class")
def navigate_to_login(setup):
    browser, wait = setup
    browser.get("https://bbp.epfl.ch/mmb-beta")
    home_page = HomePage(*setup)
    login_button = home_page.find_login_button()
    assert login_button.is_displayed()
    login_button.click()
    wait.until(EC.url_contains("auth"))
    login_url = browser.current_url
    yield login_url

# @pytest.fixture(scope="function")
# def login(setup, navigate_to_login):
#     login_page = LoginPage(*setup)
#     login_page.go_to_login_page(navigate_to_login)
#     config = load_config()
#     user_name_field = login.find_username_field()
#     assert user_name_field.is_displayed()
#     user_name_field.send_keys(config['username'])
#     yield login_page








