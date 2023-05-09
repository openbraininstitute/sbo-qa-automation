import logging
import os
import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.home_page import HomePage
from pages.login_page import LoginPage
from util.util_base import load_config
import allure
import argparse


# The setup fixture used throughout the project
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


# Logger object fixture
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


# Fixture that navigates to the login page
@pytest.fixture(scope="function")
def login(setup, navigate_to_login):
    login_page = LoginPage(*setup)
    login_page.go_to_login_page(navigate_to_login)
    yield login_page


# Login & credentials fixture that is used throughout the project
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


# Create the login_explore fixture with username/password so that it can be re-used.
@pytest.fixture(scope="function")
def login_explore(setup, navigate_to_login):
    browser, wait = setup
    login_page = LoginPage(*setup)
    login_page.go_to_login_page(navigate_to_login)
    login_page.find_username_field().send_keys(load_config()['username'])
    login_page.find_password_field().send_keys(load_config()['password'])
    login_page.find_signin_button().click()
    wait.until(EC.url_contains("mmb-beta"))
    yield browser, wait


def pytest_addoption(parser):
    parser.addoption("--no-report", action="store_true", help="Disable report generation")


def pytest_configure(config):
    generate_report = not config.getoption("--no-report")
    if generate_report:
        # Generate report code
        config.addinivalue_line(
            "markers", "skip_on_failure: mark test to be skipped if it fails"
        )

    else:
        print("Report generation disabled")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            os.makedirs("screenshots")
        except FileExistsError:
            pass  # Directory already exists
        screenshot_path = os.path.join("screenshots", f"{item.name}.png")
        browser = item.parent.obj.browser
        browser.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, attachment_type=allure.attachment_type.PNG)


def pytest_html_report_title(report):
    report.title = "SBO Test Automation Report"


def pytest_html_results_table_row(report, cells):
    if report.failed:
        cells.insert(1, ("✘", "success"))
    elif report.failed:
        cells.insert(1, ("✔", "error"))
    else:
        cells.insert(1, ("?", "skipped"))
