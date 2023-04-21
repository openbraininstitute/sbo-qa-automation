import os
import logging
import pytest

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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
