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
import base64
from PIL import Image
from selenium import webdriver
from selenium.common import exceptions, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from pages.landing_page import LandingPage
from pages.login_page import LoginPage


def get_safe_config(config):
    safe = config.copy()
    safe["password"] = "****"
    return safe

def create_browser(pytestconfig):
    browser_name = pytestconfig.getoption("--browser-name")

    headless = pytestconfig.getoption("--headless")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1400,900")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1400,900")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument('--blink-settings=imagesEnabled=true')
        browser = webdriver.Chrome(options=options)
        browser.set_window_size(1400, 900)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1400,900")
            # Additional Firefox options for CI/CD stability
            options.set_preference("dom.webnotifications.enabled", False)
            options.set_preference("media.volume_scale", "0.0")
            options.set_preference("browser.startup.homepage", "about:blank")
            options.set_preference("startup.homepage_welcome_url", "about:blank")
            options.set_preference("startup.homepage_welcome_url.additional", "about:blank")

        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    browser.set_page_load_timeout(90)  # Increased timeout for CI/CD
    browser.set_window_size(1400, 900)  # Consistent window size for Mac 14"
    wait = WebDriverWait(browser, 30)  # Increased wait timeout

    return browser, wait

@pytest.fixture(scope="function")
def public_browsing(pytestconfig, test_config, request):
    browser, wait = create_browser(pytestconfig)
    request.node._browser = browser
    yield browser, wait, test_config["base_url"]
    browser.quit()


@pytest.fixture(scope="function")
def visit_public_pages(public_browsing, logger):
    browser, wait, base_url = public_browsing

    def _visit(path=""):
        url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        logger.info(f"Navigating to: {url}")
        browser.get(url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        return browser, wait

    return _visit, base_url


@pytest.fixture(scope="session")
def test_config(pytestconfig):
    """Gets credentials and IDS returns the correct environment-specific settings."""
    username = os.getenv("OBI_USERNAME")
    password = os.getenv("OBI_PASSWORD")
    env = pytestconfig.getoption("env")

    if not username or not password:
        raise ValueError("Username or password is missing in the configuration!")

    if env =="staging":
        base_url = "https://staging.openbraininstitute.org"
        lab_url = f"{base_url}/app/virtual-lab"
        lab_id = os.getenv("LAB_ID_STAGING")
        project_id = os.getenv("PROJECT_ID_STAGING")
        oidc_login_url = (
            "https://staging.openbraininstitute.org/auth/realms/SBO/protocol/"
            "openid-connect/auth?"
            "client_id=core-webapp-main&"
            "scope=profile%20openid%20groups&"
            "response_type=code&"
            "redirect_uri=https%3A%2F%2Fstaging.openbraininstitute.org%2Fapi%2Fauth%2Fcallback%2Fkeycloak&"
            "state=123&"  
            "code_challenge=abc&"
            "code_challenge_method=S256"
        )
    elif env == "production":
        base_url = "https://www.openbraininstitute.org"
        lab_url = f"{base_url}/app/virtual-lab"
        lab_id = os.getenv("LAB_ID_PRODUCTION")
        project_id = os.getenv("PROJECT_ID_PRODUCTION")
        oidc_login_url = (
            "https://www.openbraininstitute.org/auth/realms/SBO/protocol/"
            "openid-connect/auth?"
            "client_id=core-webapp-main&"
            "scope=profile%20openid%20groups&"
            "response_type=code&"
            "redirect_uri=https%3A%2F%2Fwww.openbraininstitute.org%2Fapi%2Fauth%2Fcallback%2Fkeycloak&"
            "state=dummy&"
            "code_challenge=dummy&"
            "code_challenge_method=S256"
        )
    else:
        raise ValueError(f"Invalid environment: {env}")

    return {
        "username": username,
        "base_url": base_url,
        "lab_url": lab_url,
        "lab_id": lab_id,
        "project_id": project_id,
        "oidc_login_url": oidc_login_url,
    }


@pytest.fixture(scope="class", autouse=True)
def setup(request, pytestconfig, test_config):
    """Fixture to set up the browser/webdriver"""
    environment = pytestconfig.getoption("env")
    base_url = test_config["base_url"]
    lab_id = test_config["lab_id"]
    project_id = test_config["project_id"]

    print(f"Starting tests in {environment.upper()} mode.")
    print(f"Base URL: {base_url}")

    browser, wait = create_browser(pytestconfig)

    request.cls.base_url = base_url
    request.cls.lab_id = lab_id
    request.cls.project_id = project_id
    request.cls.browser = browser
    request.cls.wait = wait
    request.node._browser = browser
    yield browser, wait, base_url, lab_id, project_id

    if browser is not None:
        browser.quit()


@pytest.fixture(scope="function")
def navigate_to_landing_page(public_browsing, logger, test_config):
    """Fixture to open and verify the OBI Landing Page before login."""
    browser, wait, base_url = public_browsing
    landing_page = LandingPage(
        browser=browser,
        wait=wait,
        base_url= test_config["base_url"],
        logger=logger
    )

    landing_page.go_to_landing_page()
    yield landing_page


@pytest.fixture(scope="function")
def navigate_to_login(setup, logger, request, test_config):
    """Fixture that navigates to the login page"""
    browser, wait, lab_url, lab_id, project_id = setup
    landing_page = LandingPage(browser, wait, test_config["base_url"], logger)
    
    # Navigate to landing page with retry
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            landing_page.go_to_landing_page(timeout=15)
            break
        except Exception as e:
            logger.warning(f"Landing page load attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_attempts - 1:
                raise
            time.sleep(2)
    
    # Click login button with retry
    for attempt in range(max_attempts):
        try:
            landing_page.click_go_to_lab()
            break
        except Exception as e:
            logger.warning(f"Login button click attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_attempts - 1:
                raise
            time.sleep(2)

    # Wait for redirect to login page
    try:
        WebDriverWait(browser, 60).until(
            EC.url_contains("openid-connect"),
            message="Timed out waiting for OpenID login page"
        )
        logger.info("Successfully navigated to OpenID login page")
    except TimeoutException:
        current_url = browser.current_url
        logger.error(f"Failed to reach login page. Current URL: {current_url}")
        browser.save_screenshot("/tmp/navigate_to_login_failed.png")
        raise RuntimeError(f"Cannot reach OpenID login page. Current URL: {current_url}")
    
    print("DEBUG: Returning login_page from conftest.py/navigate_to_login")
    return LoginPage(browser=browser, wait=wait, lab_url=test_config["lab_url"], logger=logger)

@pytest.fixture(scope="function")
def navigate_to_login_direct(setup, logger, test_config):
    """Navigate directly to the OIDC login page instead of the landing page."""
    browser, wait, base_url, lab_id, project_id = setup
    oidc_url = test_config["oidc_login_url"]
    logger.info(f"Navigating directly to OIDC login URL: {oidc_url}")
    
    # Clear any existing cookies/session first
    browser.delete_all_cookies()
    
    browser.get(oidc_url)
    try:
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.ID, "kc-form-wrapper"))
        )
        logger.info("Reached OIDC login page")
    except TimeoutException:
        current_url = browser.current_url
        logger.warning(f"Login form not found. Current URL: {current_url}")
        
        # Check if we're on the landing page
        if "openbraininstitute.org" in current_url and "/auth/realms/" not in current_url:
            logger.info("Detected landing page redirect. Attempting to click login button.")
            
            # Try multiple login button selectors with more variations
            login_selectors = [
                (By.XPATH, "//a[@href='/app/virtual-lab']"),
                (By.XPATH, "//a[@href='/app/virtual-lab/sync']"),
                (By.XPATH, "//a[contains(@href, 'virtual-lab')]"),
                (By.XPATH, "//button[contains(text(), 'Go to Lab')]"),
                (By.XPATH, "//a[contains(text(), 'Go to Lab')]"),
                (By.XPATH, "//button[contains(@class, 'lab')]"),
                (By.XPATH, "//a[contains(@class, 'lab')]"),
                (By.CSS_SELECTOR, "[href*='virtual-lab']"),
                (By.CSS_SELECTOR, "[data-testid*='lab']"),
                (By.XPATH, "//button[contains(text(), 'Lab')]"),
                (By.XPATH, "//a[contains(text(), 'Lab')]")
            ]
            
            login_clicked = False
            for attempt in range(3):  # Try multiple times
                logger.info(f"Attempt {attempt + 1} to find login button")
                for selector in login_selectors:
                    try:
                        login_btn = WebDriverWait(browser, 15).until(
                            EC.element_to_be_clickable(selector)
                        )
                        logger.info(f"Found login button with selector: {selector}")
                        # Try clicking with JavaScript as backup
                        try:
                            login_btn.click()
                        except:
                            browser.execute_script("arguments[0].click();", login_btn)
                        login_clicked = True
                        break
                    except TimeoutException:
                        logger.debug(f"Login button not found with selector: {selector}")
                        continue
                
                if login_clicked:
                    break
                    
                # Wait before retry
                if attempt < 2:
                    logger.warning(f"Login button not found on attempt {attempt + 1}, retrying...")
                    time.sleep(3)
            
            if not login_clicked:
                logger.error("Could not find any login button on landing page after multiple attempts")
                browser.save_screenshot("/tmp/landing_page_no_login.png")
                # Try to get page source for debugging
                try:
                    page_source = browser.page_source
                    logger.error(f"Page source length: {len(page_source)}")
                    # Look for any button or link text
                    if "lab" in page_source.lower():
                        logger.error("Found 'lab' text in page source but couldn't click button")
                except:
                    pass
                raise RuntimeError("Cannot find login button on landing page")
            
            # Wait for redirect to login page
            try:
                WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.ID, "kc-form-wrapper"))
                )
                logger.info("Successfully reached OIDC login page after clicking login button")
            except TimeoutException:
                logger.error(f"Still cannot reach login page. Final URL: {browser.current_url}")
                browser.save_screenshot("/tmp/failed_login_redirect.png")
                raise RuntimeError("Cannot reach OIDC login page after clicking login button")
        else:
            logger.error(f"Unexpected page state. URL: {current_url}")
            browser.save_screenshot("/tmp/unexpected_page_state.png")
            raise RuntimeError("Cannot reach OIDC login page - unexpected page state")

    return LoginPage(browser, wait, lab_url=test_config["lab_url"], logger=logger)


@pytest.fixture(scope="function")
def login_direct_complete(setup, navigate_to_login_direct, test_config, logger):
    """Perform direct login and return browser + wait ready for use."""
    login_page = navigate_to_login_direct
    username = test_config["username"]
    password = os.getenv("OBI_PASSWORD")

    max_login_attempts = 3
    for login_attempt in range(max_login_attempts):
        try:
            logger.info(f"Login attempt {login_attempt + 1}/{max_login_attempts}")
            login_page.perform_login(username, password)
            login_page.wait_for_login_complete(timeout=90)  # Increased timeout for CI/CD
            logger.info("Login successful!")
            break
        except TimeoutException as e:
            logger.error(f"Login attempt {login_attempt + 1} timeout. Current URL: {login_page.browser.current_url}")
            
            # Take screenshot for debugging
            login_page.browser.save_screenshot(f"/tmp/login_timeout_attempt_{login_attempt + 1}.png")
            
            # Try multiple alternative approaches
            success = False
            
            # Alternative 1: Check for virtual-lab or sync in URL
            try:
                logger.info("Alternative 1: Checking for virtual-lab/sync in URL...")
                WebDriverWait(login_page.browser, 30).until(
                    lambda d: "virtual-lab" in d.current_url or "sync" in d.current_url
                )
                logger.info("Alternative 1 succeeded - found virtual-lab/sync in URL")
                success = True
            except TimeoutException:
                logger.debug("Alternative 1 failed")
            
            # Alternative 2: Check for app/ in URL (broader check)
            if not success:
                try:
                    logger.info("Alternative 2: Checking for app/ in URL...")
                    WebDriverWait(login_page.browser, 20).until(
                        lambda d: "/app/" in d.current_url
                    )
                    logger.info("Alternative 2 succeeded - found /app/ in URL")
                    success = True
                except TimeoutException:
                    logger.debug("Alternative 2 failed")
            
            # Alternative 3: Look for logged-in indicators on page
            if not success:
                try:
                    logger.info("Alternative 3: Looking for logged-in page elements...")
                    WebDriverWait(login_page.browser, 15).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid*='user']")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid*='lab']")),
                            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Logout')]")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='virtual-lab']"))
                        )
                    )
                    logger.info("Alternative 3 succeeded - found logged-in page elements")
                    success = True
                except TimeoutException:
                    logger.debug("Alternative 3 failed")
            
            # Alternative 4: Manual navigation to virtual lab
            if not success and login_attempt < max_login_attempts - 1:
                try:
                    logger.info("Alternative 4: Manually navigating to virtual lab...")
                    lab_url = test_config["lab_url"]
                    login_page.browser.get(lab_url)
                    WebDriverWait(login_page.browser, 20).until(
                        lambda d: "virtual-lab" in d.current_url or "sync" in d.current_url
                    )
                    logger.info("Alternative 4 succeeded - manual navigation worked")
                    success = True
                except Exception as nav_error:
                    logger.debug(f"Alternative 4 failed: {nav_error}")
            
            if success:
                logger.info("Login completed via alternative method")
                break
            elif login_attempt == max_login_attempts - 1:
                logger.error("All login attempts and alternatives failed")
                raise e
            else:
                logger.warning(f"Login attempt {login_attempt + 1} failed, retrying...")
                time.sleep(5)  # Wait before retry

    browser, wait, base_url, lab_id, project_id = setup
    yield browser, wait, base_url, lab_id, project_id

@pytest.fixture(scope="function")
def login(setup, navigate_to_login, test_config, logger):
    """Fixture to log in and ensure user is authenticated."""
    browser, wait, lab_url, lab_id, project_id = setup
    login_page = navigate_to_login

    username = test_config.get("username")
    password = os.getenv("OBI_PASSWORD")

    if not username or not password:
        raise ValueError("Username or password is missing in the configuration!")

    login_page.perform_login(test_config["username"], password)
    login_page.wait_for_login_complete()
    print("Login successful. Current URL:", browser.current_url)
    login_page = LoginPage(browser, wait, lab_url, logger)

    yield browser, wait
    login_page.browser.delete_all_cookies()

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


failed_tests = []

def pytest_runtest_logstart(nodeid, location):
    """Hook to clearly display the test file starting"""
    test_file = location[0].upper()
    print(f"\033[95m\n🚀 STARTING TEST FILE: {test_file}\033[0m\n")


def pytest_runtest_logreport(report):
    """Capture failed tests during runtime"""
    if report.failed and report.when in ("setup", "call", "teardown"):
        failed_tests.append(report.nodeid)

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print failed test summary at the very end of the session output."""
    if failed_tests:
        terminalreporter.write_line("")  # just spacing
        terminalreporter.write_sep("=", "❌ FAILED TEST SUMMARY", red=True)
        for test in failed_tests:
            terminalreporter.write_line(f"- {test}", red=True)
    else:
        terminalreporter.write_line("")
        terminalreporter.write_sep("=", "✅ ALL TESTS PASSED", green=True)


# def pytest_sessionfinish(session, exitstatus):
#     """Print failed test summary at the end of the session"""
#     if failed_tests:
#         print("\n\033[91m❌ FAILED TEST SUMMARY:\033[0m")
#         for test in failed_tests:
#             print(f"\033[91m- {test}\033[0m")
#     else:
#         print("\n\033[92m✅ ALL TESTS PASSED\033[0m")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook implementation to handle test reporting.

    - Captures screenshots when a test fails.
    - Embeds the screenshot into the HTML report.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    if not pytest_html:
        print("pytest-html plugin not available.")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    # if report.when == 'call' or report.when == "setup":
    if report.when in ("setup", "call", "teardown"):
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
                print(f"Browser found in item attribute", report.nodeid)

            if browser:
                try:
                    print("Browser object found - making screenshot")
                    _capture_screenshot(file_name, browser)
                    if os.path.exists(file_name):
                        print(f"Screenshot successfully saved at: {file_name}")
                        # html = ('<div><img src="%s" alt="screenshot" '
                        #         'style="width:304px;height:228px;" onclick="window.open(this.src)" '
                        #         'align="right"/></div>') % os.path.relpath(file_name)
                        with open(file_name, "rb") as image_file:
                            encoded = base64.b64encode(image_file.read()).decode("utf-8")
                            html = f'<div><img src="data:image/png;base64,{encoded}" ' \
                                   f'style="width:304px;height:228px;" onclick="window.open(this.src)" align="right"/></div>'
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

def mask_sensitive(config):
    """Mask sensitive keys like 'password' before logging."""
    return {k: (v if "pass" in k.lower() else "***") for k, v in config.items()}
