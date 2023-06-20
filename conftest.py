import json
import logging
import os
import pytest
from selenium import webdriver
from seleniumbase import BaseCase
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.home_page import HomePage
from pages.login_page import LoginPage
from util.util_base import load_config
import allure
import argparse
import glob



@pytest.fixture(scope="class")
def setup(request, pytestconfig):
    browser_name = os.environ.get("BROWSER_NAME")
    headless_mode = pytestconfig.getoption("--headless")

    if browser_name == "chrome":
        if "chromedriver" in os.environ.get("PATH", ""):
            options = ChromeOptions()
            if headless_mode:
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-gpu")
            browser = webdriver.Chrome(options=options)
        else:
            options = ChromeOptions()
            if headless_mode:
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-gpu")
            browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        if "geckodriver" in os.environ.get("PATH", ""):
            options = FirefoxOptions()
            if headless_mode:
                options.add_argument("--headless=new")
            executable_path = GeckoDriverManager().install()
            browser = webdriver.Firefox(options=options, executable_path=executable_path)
        else:
            options = FirefoxOptions()
            if headless_mode:
                options.add_argument("--headless=new")
            browser = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Invalid browser name: {browser_name}")


# @pytest.fixture(scope="class")
# def setup(request):
#     # Check if geckodriver or chromedriver is available
#     if "geckodriver" in os.environ.get("PATH", ""):
#         # Use Firefox driver
#         options = FirefoxOptions()
#         browser = webdriver.Firefox(options=options)
#     elif "chromedriver" in os.environ.get("PATH", ""):
#         # Use Chrome driver
#         options = ChromeOptions()
#         browser = webdriver.Chrome(options=options)
#     else:
#         # No driver available, run in headless mode without a browser
#         options = FirefoxOptions()
#         options.add_argument("--headless=new")
#         options.add_argument("--disable-gpu")
#         options.add_argument("--sandbox-no")
#         browser = webdriver.Firefox(options=options)
    # Setting explicit wait
    wait = WebDriverWait(browser, 10)
    browser.set_window_position(-1000, 0)
    browser.maximize_window()
    request.cls.browser = browser
    request.cls.wait = wait
    yield browser, wait

    browser.quit()

def pytest_addoption(parser):
    parser.addoption("--no-report", action="store_true", help="Disable report generation")


# Logger object fixture
@pytest.fixture(scope="module")
def logger(request):
    # Initialize the logger object
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Check if the logger already has a file handler
    has_file_handler = any(isinstance(handler, logging.FileHandler) for handler in logger.handlers)

    # Determine the outer allure_reports directory
    allure_reports_dir = request.config.getoption("--alluredir")

    if not has_file_handler:
        # Create the outer allure_reports directory if it doesn't exist
        os.makedirs(allure_reports_dir, exist_ok=True)

        # Create the log file path
        log_file_path = os.path.join(allure_reports_dir, "report.log")

        # Create the log file handler
        file_handler = logging.FileHandler(filename=log_file_path)
        file_handler.setLevel(logging.DEBUG)
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


@pytest.fixture(scope="function")
def navigate_to_login(setup):
    browser, wait = setup
    print(f"What is {setup}")
    browser.get("https://bbp.epfl.ch/mmb-beta")
    home_page = HomePage(*setup)
    login_button = home_page.find_login_button()
    assert login_button.is_displayed()
    login_button.click()
    wait.until(EC.url_contains("auth"))
    login_url = browser.current_url
    yield login_url


@pytest.fixture(scope="function")
def login_explore(navigate_to_login, setup):
    browser, wait = setup
    login_page = LoginPage(*setup)
    login_page.go_to_login_page(navigate_to_login)

    config = load_config()
    username = config['username']
    password = config['password']

    login_page.find_username_field().send_keys(username)
    login_page.find_password_field().send_keys(password)
    login_page.find_signin_button().click()
    wait.until(EC.url_contains("mmb-beta"))
    yield browser, wait


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        screenshot_dir = os.path.join("allure_reports", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
        browser = item.parent.obj.browser
        browser.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, attachment_type=allure.attachment_type.PNG)
        # Custom logging to report.log
        logger = logging.getLogger(__name__)
        logger.info("Test failed: %s", item.name)
        logger.info("Failure description: %s", rep.longreprtext)

def pytest_html_results_table_row(report, cells):
    if report.failed:
        cells.insert(1, ("✘", "success"))
    elif report.failed:
        cells.insert(1, ("✔", "error"))
    else:
        cells.insert(1, ("?", "skipped"))



def delete_previous_reports(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)  # Create the directory if it doesn't exist
        os.chdir(folder_path)

        file_list = glob.glob("*")
        file_list.sort(key=os.path.getmtime)

        files_to_delete = file_list[:-3]
        for file_name in files_to_delete:
            os.remove(file_name)
    except OSError as e:
        print(f"Error deleting previous reports: {e}")

# Specify the folder path where the allure reports are stored
folder_path = "allure_reports/allure_reports"

# Call the function to delete previous reports
delete_previous_reports(folder_path)

