import json
import logging
import os
from io import BytesIO

import pytest
from PIL import Image
from selenium import webdriver
from selenium.common import exceptions, NoSuchElementException
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
def navigate_to_login(setup):
    browser, wait = setup
    browser.get("https://bbp.epfl.ch/mmb-beta")
    home_page = HomePage(*setup)
    browser.delete_all_cookies()

    login_button = home_page.find_login_button()
    assert login_button.is_displayed()
    login_btn = login_button.text
    assert login_btn == 'Login'
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
            print("Test failed - handling it")
            file_name = "latest_logs/" + report.nodeid.replace("::", "_") + ".png"
            if hasattr(item, "cls"):
                browser = getattr(item.cls, "browser", None)
            if not browser:
                browser = getattr(item, "_browser", None)
            if browser:
                print("Browser object found - making screenshot")
                _capture_screenshot(file_name, browser)
                if file_name:
                    html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % file_name
                    extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name, browser):
    os.makedirs(os.path.dirname(name), exist_ok=True)
    browser.get_full_page_screenshot_as_file(name)


# Hook to customize the HTML report table row cells
def pytest_html_results_table_row(report, cells):
    if report.failed:
        cells.insert(1, ("✘", "fail"))
    # elif report.failed:
        # cells.insert(1, ("✔", "error"))
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


# Add custom markers
def pytest_collection_modifyitems(config, items):
    config.addinivalue_line(
        "markers", "explore_page: mark a test as an explore_page test"
    )
    config.addinivalue_line(
        "markers", "build_page: mark a test as a build_page test"
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
