# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
import json
import logging
import os
import sys
import time
from io import BytesIO

import pytest
from PIL import Image
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from pages.landing_page import LandingPage
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def test_config(pytestconfig):
    """Gets credentials and IDS returns the correct environment-specific settings."""
    username = os.getenv("OBI_USERNAME")
    password = os.getenv("OBI_PASSWORD")
    env = pytestconfig.getoption("env")

    if not username or not password:
        raise ValueError("Username or password is missing in the configuration!")

    if env =="staging":
        landing_url = "https://staging.openbraininstitute.org"
        base_url = "https://staging.openbraininstitute.org/app/virtual-lab"
        lab_id = os.getenv("LAB_ID_STAGING")
        project_id = os.getenv("PROJECT_ID_STAGING")
    elif env == "production":
        landing_url = "https://www.openbraininstitute.org"
        base_url = "https://www.openbraininstitute.org/app/virtual-lab"
        lab_id = os.getenv("LAB_ID_PRODUCTION")
        project_id = os.getenv("PROJECT_ID_PRODUCTION")
    else:
        raise ValueError(f"Invalid environment: {env}")

    return {
        "username": username,
        "password": password,
        "landing_url": landing_url,
        "base_url": base_url,
        "lab_id": lab_id,
        "project_id": project_id,
    }


@pytest.fixture(scope="class", autouse=True)
def setup(request, pytestconfig, test_config):
    """Fixture to set up the browser/webdriver"""
    environment = pytestconfig.getoption("env")
    browser_name = pytestconfig.getoption("--browser-name")
    base_url = test_config["base_url"]
    lab_id = test_config["lab_id"]
    project_id = test_config["project_id"]

    print(f"Starting tests in {environment.upper()} mode.")
    print(f"Base URL: {base_url}")

    if browser_name == "chrome":
        options = ChromeOptions()
        if pytestconfig.getoption("--headless"):
            options.add_argument("--headless")
            options.add_argument("--ignore-certificate-errors")
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if pytestconfig.getoption("--headless"):
            options.add_argument("--headless")
        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    browser.set_page_load_timeout(60)
    wait = WebDriverWait(browser, 20)

    request.cls.base_url = base_url
    request.cls.lab_id = lab_id
    request.cls.project_id = project_id

    request.cls.browser = browser
    request.cls.wait = wait

    if not request.node.get_closest_marker("no_auto_nav"):
        print(f"Navigating to Base URL (default): {base_url}")
        browser.get(base_url)
    else:
        print("Skipping automatic navigation to base_url (no_auto_nav)")

    yield browser, wait, base_url, lab_id, project_id

    if browser is not None:
        browser.quit()


@pytest.fixture(scope="function")
def logger(request):
    """Fixture to initialize the logger object"""
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    project_root = os.path.abspath(os.path.dirname(__file__))
    allure_reports_dir = os.path.join(project_root, "allure_reports")
    log_file_path = os.path.join(allure_reports_dir, "report.log")
    if not os.path.exists(allure_reports_dir):
        os.makedirs(allure_reports_dir)

    # Check if logger already has handlers
    if not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
        file_handler = logging.FileHandler(filename=log_file_path)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter("%(levelname)s : %(asctime)s : %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_formatter = logging.Formatter("\n%(levelname)s : %(asctime)s : %(message)s")
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    logger.info("🟢 Test started")

    def log_test_finish():
        logger.info("🛑 Test finished")

    request.addfinalizer(log_test_finish)

    return logger


@pytest.fixture(scope="function")
def navigate_to_landing_page(setup, logger, test_config):
    """Fixture to open and verify the OBI Landing Page before login."""
    browser, wait, base_url, lab_id, project_id = setup
    landing_page = LandingPage(browser, wait, base_url, test_config["landing_url"], logger)

    landing_page.go_to_landing_page()
    yield landing_page


@pytest.fixture(scope="function")
def navigate_to_login(setup, logger, request, test_config):
    """Fixture that navigates to the login page"""
    browser, wait, base_url, lab_id, project_id = setup
    login_page = LoginPage(browser, wait, base_url, logger)

    if request.node.get_closest_marker("use_landing_page"):
        landing_page = LandingPage(browser, wait, base_url, test_config["landing_url"], logger)
        landing_page.go_to_landing_page()
        print(f"INFO: Landing page visited, current URL: {browser.current_url}")
        landing_page.click_go_to_lab()
        print(f"INFO: After clicking go to lab, current URL: {browser.current_url}")
    else:
        browser.get(f"{base_url}")
        print(f"INFO: Direct access to base URL: {base_url}")
    print(f"INFO: Waiting for OpenID login redirect, current URL: {browser.current_url}")

    login_page.wait_for_condition(
        lambda driver: "openid-connect" in driver.current_url,
        timeout=60,
        retries=3,
        delay=5,
        message="Timed out waiting for OpenID login page."
    )
    print("DEBUG: Returning login_page from conftest.py/navigate_to_login")
    return login_page

@pytest.fixture(scope="function")
def login(setup, navigate_to_login, test_config, logger):
    """Fixture to log in and ensure user is authenticated."""
    browser, wait, base_url, lab_id, project_id = setup
    login_page = navigate_to_login

    username = test_config.get("username")
    password = test_config.get("password")

    if not username or not password:
        raise ValueError("Username or password is missing in the configuration!")

    login_page.perform_login(username, password)
    login_page.wait_for_login_complete()
    print("Login successful. Current URL:", browser.current_url)
    login_page = LoginPage(browser, wait, base_url, logger)
    modal_terms_and_conditions = login_page.terms_modal()
    assert modal_terms_and_conditions.is_displayed(), "The TOR modal is not displayed for 1st time users"

    if modal_terms_and_conditions:
        print("Modal appeared for first-time users")
        modal_tor_link = login_page.terms_modal_link()
        logger.info('Terms and conditions links is displayed')
        modal_continue_btn = login_page.terms_modal_continue()
        modal_continue_btn.click()
        logger.info("Continue button is clicked")
    else:
        print("Modal did NOT appear")
    yield browser, wait
    login_page.browser.delete_all_cookies()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook implementation to handle test reporting.

    - Captures screenshots when a test fails.
    - Embeds the screenshot into the HTML report.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            print("Test failed - handling it")

            project_root = os.path.abspath(os.path.dirname(__file__))
            error_logs_dir = os.path.join(project_root, "latest_logs", "errors")
            os.makedirs(error_logs_dir, exist_ok=True)

            test_name = report.nodeid.replace("::", "_").split("/")[-1]
            file_name = os.path.join(error_logs_dir, test_name + ".png")
            print(f"Intended screenshot path: {file_name}")

            browser = None
            if hasattr(item, "cls"):
                browser = getattr(item.cls, "browser", None)
            if not browser:
                browser = getattr(item, "_browser", None)
                print(f"Browser found in item attribute")

            if browser:
                try:
                    print("Browser object found - making screenshot")
                    _capture_screenshot(file_name, browser)
                    if os.path.exists(file_name):
                        print(f"Screenshot successfully saved at: {file_name}")
                        html = ('<div><img src="%s" alt="screenshot" '
                                'style="width:304px;height:228px;" onclick="window.open(this.src)" '
                                'align="right"/></div>') % os.path.relpath(file_name)
                        extra.append(pytest_html.extras.html(html))
                    else:
                        print(f"Screenshot not found at: {file_name}")
                except Exception as e:
                    print(f"Exception occurred while capturing screenshot: {e}")
            else:
                print("No browser object found - skipping screenshot capture")

        report.extra = extra


def _capture_screenshot(name, browser):
    """
        Helper function to capture and save a screenshot.

        - Ensures the target directory exists.
        - Uses the browser object to capture a full-page screenshot.
        :param name: The full path where the screenshot will be saved.
        :param browser: The browser object used for screenshot capture.
        """
    try:
        print(f"Creating error  directory at:{os.path.dirname(name)}")
        os.makedirs(os.path.dirname(name), exist_ok=True)
        print(f"Saving screenshot to: {name}")
        # browser.get_full_page_screenshot_as_file(name)
        browser.save_screenshot(name)
        print(f"Screenshot captured: {name}")
    except Exception as e:
        print(f"Failed to capture screenshot '{name}': {e}")


def pytest_html_results_table_row(report, cells):
    """Styling for html report
    Hook to customize the HTML report table row cells
    """
    if report.failed:
        cells.insert(1, ("✘", "fail"))
    else:
        cells.insert(1, ("?", "skipped"))


def pytest_sessionstart(session):
    """ Hook to delete previous allure reports before running the tests"""
    try:
        project_root = os.path.abspath(os.path.dirname(__file__))
        folder_path = os.path.join(project_root, "allure_reports")
        if os.path.exists(folder_path) and os.listdir(folder_path):
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
    except Exception as e:
        print(f"Failed to clear allure reports: {e}")


def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        action="store",
        default="chrome",
        choices=["firefox", "chrome", "safari", "edge"],
        help="Specify the browser to run the tests in",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--log-file-path",
        action="store",
        default=None,
        help="Specify the log file path"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:4444/wd/hub",
        help="BAse URL for the Selenium Webdriver server")

    parser.addoption(
        "--env",
        action="store",
        default="local",
        choices=["local", "staging", "production", "sauce-labs"],
        help="Specify the environment to run the tests in"
    )
    parser.addoption(
        "--env_url",
        action="store",
        default="production",
        choices=["staging", "production"],
        help="Specify the environment URL: staging or production"
    )


def make_full_screenshot(browser, savename):
    """Performs a full screenshot of the entire page.
    Taken from https://gist.github.com/fabtho/13e4a2e7cfbfde671b8fa81bbe9359fb
    """
    logger.debug('Making full-page screenshot')
    # initiate value
    img_list = []  # to store image fragment
    offset = 0  # where to start

    # js to get height of the window
    try:
        height = browser.execute_script(
            "return Math.max("
            "document.documentElement.clientHeight, window.innerHeight);"
        )
    except exceptions.WebDriverException:
        return

    max_window_height = browser.execute_script(
        "return Math.max("
        "document.body.scrollHeight, "
        "document.body.offsetHeight, "
        "document.documentElement.clientHeight, "
        "document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )

    header_height = 0
    while offset < max_window_height:
        browser.execute_script(f"window.scrollTo(0, {offset});")

        # get the screenshot of the current window
        img = Image.open(BytesIO((browser.driver.get_screenshot_as_png())))
        img_list.append(img)
        offset += height - header_height

    # Stitch image into one, set up the full screen frame
    img_frame_height = sum([img_frag.size[1] for img_frag in img_list])
    img_frame = Image.new("RGB", (img_list[0].size[0], img_frame_height))

    offset = 0  # offset used to create the snapshots
    img_loc = 0  # offset used to create the final image
    for img_frag in img_list:
        # image fragment must be cropped in case the page is a jupyter notebook;
        # also make sure the last image fragment gets added correctly to avoid overlap.
        offset1 = offset + height
        if offset1 > max_window_height:
            top_offset = offset + height - max_window_height
            box = (0, top_offset, img_frag.size[0], img_frag.size[1])
        else:
            box = (0, header_height, img_frag.size[0], img_frag.size[1])
        img_frame.paste(img_frag.crop(box), (0, img_loc))
        img_loc += img_frag.size[1] - header_height
        offset += height - header_height

    # Save the final image
    img_frame.save(savename)


@pytest.fixture(scope="session", autouse=True)
def check_skip_condition():
    """ Skips a test file from running"""
    import os
    if os.getenv("SKIP_MODULES") == "1":
        pytest.skip("Skipping tests due to global configuration.", allow_module_level=True)
