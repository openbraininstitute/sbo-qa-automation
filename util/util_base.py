import os
import logging
import pytest

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# @pytest.fixture(scope="session", params=["chrome", "firefox"])
# def driver(request):
#     if request.param == "chrome":
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--start-maximized')
#         driver = webdriver.Chrome(options=options)
#     elif request.param == "firefox":
#         options = webdriver.FirefoxOptions()
#         options.headless = True
#         driver = webdriver.Firefox(options=options)
#     driver.maximize_window()
#     yield driver
#     driver.quit()


# @pytest.fixture(scope="module")
# def logger():
#     logging.basicConfig(level=logging.INFO)
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.DEBUG)
#     console_formatter = logging.Formatter("%s(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     console_handler.setFormatter(console_formatter)
#     logger.addHandler(console_handler)
#
#     file_handler = logging.FileHandler(filename='test.log')
#     file_handler.setLevel(logging.INFO)
#     file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     file_handler.setFormatter(file_formatter)
#     logger.addHandler(file_handler)
#
#     return logger


# @pytest.fixture(scope="function")
# def wait(driver):
#     wait = WebDriverWait(driver, timeout=10)
#     yield wait

# @pytest.fixture(scope="function")
# def home_page(setup):
#     driver, wait = setup
#     from pages.home_page import HomePage
#     home_page = HomePage(driver, wait)
#     home_page.go_to_home_page()
#     return home_page


