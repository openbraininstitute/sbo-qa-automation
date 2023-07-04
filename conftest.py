import json
import logging
import os
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pages.home_page import HomePage
from pages.login_page import LoginPage
from util.util_base import load_config
import allure
import argparse
import glob


# Fixture to set up the browser
@pytest.fixture(scope="class", autouse=True)
def setup(request, pytestconfig):
    browser_name = os.environ.get("BROWSER_NAME")
    print("BROWSER_NAME******", browser_name)
    headless_mode = pytestconfig.getoption("--headless")
    browser = None
    options = ChromeOptions()  # Default to Chrome options

    if browser_name == "chrome":
        if headless_mode:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        service = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless_mode:
            options.add_argument("--headless")
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        browser = webdriver.Firefox(service=service, options=options)
    elif browser_name == "headless":
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        service = ChromeService(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)

    else:
        raise ValueError("Invalid BROWSER_NAME: {}".format(browser_name))

    wait = WebDriverWait(browser, 10)

    if browser is not None:
        browser.set_window_position(-1000, 0)
        browser.maximize_window()
    browser.delete_all_cookies()

    request.cls.browser = browser
    request.cls.wait = wait
    yield browser, wait

    if browser is not None:
        browser.quit()


# Fixture to initialize the logger object
@pytest.fixture(scope="function")
def logger(request):
    # Initialize the logger object
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
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
def navigate_to_login(setup, logger):
    browser, wait = setup
    browser.get("https://bbp.epfl.ch/mmb-beta")
    home_page = HomePage(*setup)
    browser.delete_all_cookies()
    try:
        logger.info('Looking for login button')
        login_button = home_page.find_login_button()
        login_btn = login_button.text
        assert login_btn == 'Login'

    except NoSuchElementException:
        logger.info('Login button not found - assuming already logged in')
        return
    logger.debug('Login button found: {}'.format(login_button))
    login_button = home_page.find_login_button()
    login_btn = login_button.text
    assert login_btn == 'Login'
    login_button.click()
    tst_url = wait.until(EC.url_contains("auth"))
    login_url = browser.current_url
    print("Navigate_to_login-------------------------", login_url)
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
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            browser = getattr(item, "_browser", None)
            if browser:
                _capture_screenshot(file_name, browser)
                if file_name:
                    html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % file_name
                    extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name, browser):
    browser.get_screenshot_as_file(name)


# Hook to customize the HTML report table row cells
def pytest_html_results_table_row(report, cells):
    if report.failed:
        cells.insert(1, ("✘", "success"))
    elif report.failed:
        cells.insert(1, ("✔", "error"))
    else:
        cells.insert(1, ("?", "skipped"))


# Hook to delete previous allure reports before running the tests
def pytest_sessionstart(session):
    folder_path = session.config.getoption("--alluredir")
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))


# Command-line options
def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        action="store",
        default="firefox",
        choices=["firefox"],
        help="Specify the browser to run the tests in",
    )

    parser.addoption("--log-file-path", action="store", default=None, help="Specify the log file path")


# Remove the pytest_html plugin hook
# def pytest_configure(config):
#     config.addinivalue_line(
#         "markers", "explore_page: mark a test as an explore_page test"
#     )
#     config.addinivalue_line(
#         "markers", "build_page: mark a test as a build_page test"
#     )
#     os.environ["BROWSER_NAME"] = config.getoption("--browser")


# Add custom markers
def pytest_collection_modifyitems(config, items):
    config.addinivalue_line(
        "markers", "explore_page: mark a test as an explore_page test"
    )
    config.addinivalue_line(
        "markers", "build_page: mark a test as a build_page test"
    )


# Custom report generation
# def pytest_terminal_summary(terminalreporter, config):
#     if not terminalreporter.config.option.no_report:
#         terminalreporter.config.pluginmanager.get_plugin("seleniumbase_reporter")


# Delete previous allure reports before generating new reports
def pytest_sessionfinish(session, exitstatus):
    if exitstatus == pytest.ExitCode.OK:
        reports_folder = session.config.getoption("--alluredir")
        if os.path.exists(reports_folder):
            for root, dirs, files in os.walk(reports_folder):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))


