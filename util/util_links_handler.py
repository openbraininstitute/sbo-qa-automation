import os
import json
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

class LinkHandler:
    def __init__(self, browser):
        self.browser = browser
        self.session = requests.Session()
        self.valid_status_codes = range(200, 500)


    def test_links_on_page(self, url):
        """Navigates to a page, extracts links, and checks status codes."""
        print(f"\n[INFO] Testing links on: {url}")
        self.browser.get(url)

        # Extract all links on the page
        links = self.link_handler.scrape_links()
        assert links, f"No links found on {url}!"

        # Validate links
        self.link_handler.check_links(links)
