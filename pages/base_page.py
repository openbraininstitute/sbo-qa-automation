# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import pytest
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("setup", "logger")
class CustomBasePage:

    def __init__(self, browser, wait, lab_url):
        self.browser = browser
        self.wait = wait
        # self.logger = logger
        self.lab_url = lab_url
        self.browser.set_page_load_timeout(60)

    def go_to_page(self, page_url):
        if self.lab_url is None:
            raise ValueError("lab_url is not set. Cannot navigate to page.")

        url = self.lab_url + page_url
        print(f"INFO: CustomPage base_url + page_url = {url}" )
        self.browser.get(url)

    def assert_visible(self, element, description, file_path=None, line=None):
        if not element.is_displayed():
            loc = f"{file_path}:{line}" if file_path and line else ""
            raise AssertionError(f"❌ {description} not visible {f'@ {loc}' if loc else ''}")
        else:
            # self.logger.info(f" {description} is visible.")
            print(f"{description} is visible.")

    def find_element(self, by_locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located(by_locator)
        )

    def element_visibility(self, by_locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located(by_locator)
        )

    def visibility_of_all_elements(self, by_locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_all_elements_located(by_locator)
        )

    def find_all_elements(self, by_locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_all_elements_located(by_locator)
        )

    def element_to_be_clickable(self, by_locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable(by_locator)
        )

    def assert_element_text(self, by_locator, expected_text):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        assert element.text == expected_text

    def is_enabled(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        return element.is_enabled()

    def enter_text(self, by_locator, text):
        return self.wait.until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def is_visible(self, by_locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(by_locator)
        )

    def text_is_visible(self, by_locator, text, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
        EC.text_to_be_present_in_element(by_locator, text)
        )

    def wait_for_long_load(self, element_locator, timeout=60):
        try:
            print(f"Waiting for element: {element_locator}")
            return WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located(element_locator)
            )
        except TimeoutException as ex:
            raise Exception(f"Element {element_locator} not visible after {timeout} seconds. Exception: {ex}")

    def wait_for_page_ready(self, timeout=20):
        """
        Waits until the page's readyState is 'complete', indicating that the page has finished loading.

        Args:
            timeout (int): Maximum time to wait for the page to be ready.

        Returns:
            bool: True if the page is ready within the timeout, False otherwise.
        """
        return self.wait.until(
            lambda driver: self.browser.execute_script("return document.readyState") == "complete",
            f"Page did not reach ready state within {timeout} seconds"
        )

    def wait_for_page_to_load(self, timeout=10, element_locator=None):
        local_wait = WebDriverWait(self.browser, timeout)
        local_wait.until(
            lambda driver: self.browser.execute_script("return document.readyState") == "complete",
            f"Page did not reach ready state within {timeout} seconds"
        )
        if element_locator:
            local_wait.until(EC.visibility_of_element_located(element_locator))

    def wait_for_condition(self, condition, timeout=60, retries=3, delay=5, message=None):
        """
        General-purpose wait function to wait for a specific condition with retries.

        :param condition: The condition to wait for (e.g., element presence, URL contains).
        :param timeout: How long to wait before timing out (in seconds).
        :param retries: How many times to retry if the condition isn't met (default is 3).
        :param delay: Delay in seconds between retries (default is 5 seconds).
        :param message: Custom error message if timeout occurs.
        :return: The result of the condition (e.g., an element or True).
        """
        attempt = 0
        while attempt < retries:
            try:
                print(f"Attempt {attempt + 1}/{retries} to wait for condition.")
                return self.wait.until(condition, message)
            except TimeoutException:
                if attempt < retries - 1:
                    print(f"Condition not met. Retrying in {delay} seconds...")
                    time.sleep(delay)
                attempt += 1
        raise RuntimeError(message or f"Condition not met within {timeout} seconds after {retries} retries.")

    def wait_for_url_contains(self, url_fragment: str, timeout: int = 30):
        WebDriverWait(self.browser, timeout).until(
            EC.url_contains(url_fragment),
            message=f"Timed out waiting for URL to contain: '{url_fragment}'"
        )

    def wait_for_url_change(self, old_url, timeout=30):
        return self.wait.until(
            lambda driver: driver.current_url != old_url,
            timeout
        )

    def is_clickable_via_js(self, element):
        """
        Checks if an element is not covered by another element at its center point.
        Returns True if the element is the topmost element at its center.
        """
        return self.browser.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const x = rect.left + (rect.width / 2);
            const y = rect.top + (rect.height / 2);
            const elAtCenter = document.elementFromPoint(x, y);
            return elAtCenter === arguments[0];
        """, element)

    def scroll_into_view_and_click(self, locator, timeout=10):
        el = self.element_to_be_clickable(locator, timeout=timeout)
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        el.click()
        return el

    def wait_and_click(self, by_locator, timeout=20):
        """Wait until element is visible and enabled, then click (with JS fallback)."""
        try:

            WebDriverWait(self.browser, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)

            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(by_locator)
            )
            WebDriverWait(self.browser, timeout).until(
                EC.element_to_be_clickable(by_locator)
            )

            elem = self.browser.find_element(*by_locator)
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
            time.sleep(2)

            try:
                elem.click()
            except Exception as click_error:
                print(f"Standard click failed: {click_error}. Trying JavaScript click...")
                self.browser.execute_script("arguments[0].click();", elem)

            return

        except Exception as e:
            timestamp = int(time.time())
            self.browser.save_screenshot(f"error_wait_and_click_{timestamp}.png")
            with open(f"error_wait_and_click_{timestamp}.html", "w", encoding="utf-8") as f:
                f.write(self.browser.page_source)

            try:
                elem = self.browser.find_element(*by_locator)
                location = elem.location_once_scrolled_into_view
                top_element = self.browser.execute_script(
                    "return document.elementFromPoint(arguments[0], arguments[1]);",
                    location['x'], location['y']
                )
                print("Top element at click point:", top_element.get_attribute('outerHTML'))
            except Exception as diag_error:
                print("Could not inspect top element:", diag_error)

            try:
                for entry in self.browser.get_log('browser'):
                    print(entry)
            except Exception as log_error:
                print("Browser logs not available:", log_error)

            raise TimeoutException(f"Element {by_locator} was not clickable after {timeout}s. Error: {e}")

    def wait_for_image_to_load(self, img_locator, timeout=20):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.find_element(*img_locator).get_attribute("src") and
                           driver.find_element(*img_locator).is_displayed()
        )

    def wait_for_video_to_load(self, video_locator, timeout=20):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.execute_script(
                "const video = arguments[0]; return video.readyState >= 3;",
                driver.find_element(*video_locator)
            )
        )

    def find_child_elements(self, parent_element, by_locator, timeout=10):
        """
        Finds child elements within a given parent element, waiting for them to fully load.
        """
        WebDriverWait(self.browser, timeout).until(
            lambda driver: len(parent_element.find_elements(*by_locator)) > 0
        )
        return parent_element.find_elements(*by_locator)

    def wait_for_element_to_disappear(self, by_locator, timeout=30):
        """Wait for the element to disappear (become invisible) using explicit wait."""
        WebDriverWait(self.browser, timeout).until(
            EC.invisibility_of_element_located(by_locator),
            message=f"Element {by_locator} did not disappear within {timeout} seconds."
        )

    def wait_for_non_empty_text(self, locator, timeout=25):
        def check_text(d):
            element = d.find_element(*locator)
            print(f"Checking text for {locator}: '{element.text.strip()}'")
            return element if element.text.strip() else False

        return WebDriverWait(self.browser, timeout).until(check_text)

    def _get_counts_with_retry(self, record_count_locators, timeout):
        record_counts = []
        for locator in record_count_locators:
            try:
                print(f"Waiting for record count element: {locator}")
                record = self.wait_for_non_empty_text(locator, timeout)
                record_text = record.text.strip()
                print(f"Found text for {locator}: '{record_text}'")
                record_number = int(''.join(filter(str.isdigit, record_text)))
                record_counts.append(record_number)
            except TimeoutException:
                raise TimeoutException(f"Timeout: No text found for record at {locator} within {timeout} seconds.")
            except ValueError:
                raise ValueError(f"Could not parse record count from text: '{record_text}'")
        return record_counts