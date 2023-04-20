import os
import logging
import pytest

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait



@pytest.fixture(scope="module")
def setup():
    browser = webdriver.Chrome()
    logging.basicConfig(level=logging.INFO)
    wait = WebDriverWait(browser, 10)
    yield browser, wait, logging

    browser.quit()