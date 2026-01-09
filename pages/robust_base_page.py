# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import time
from selenium.common import TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import CustomBasePage


class RobustBasePage(CustomBasePage):
    """Enhanced base page with robust error handling for CI/CD environments."""
    
    def __init__(self, browser, wait, base_url, logger=None):
        super().__init__(browser, wait, base_url)
        self.logger = logger
        
    def robust_find_element(self, locator, timeout=30, max_attempts=3):
        """Find element with retry mechanism for CI/CD stability."""
        for attempt in range(max_attempts):
            try:
                element = WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_element_located(locator)
                )
                # Additional check for element visibility
                if element.is_displayed():
                    return element
                else:
                    if self.logger:
                        self.logger.warning(f"Element found but not visible on attempt {attempt + 1}")
                    if attempt < max_attempts - 1:
                        time.sleep(2)
                        continue
                    return element
                    
            except (TimeoutException, StaleElementReferenceException) as e:
                if self.logger:
                    self.logger.warning(f"Attempt {attempt + 1} failed to find element {locator}: {str(e)}")
                if attempt == max_attempts - 1:
                    raise TimeoutException(f"Failed to find element {locator} after {max_attempts} attempts")
                time.sleep(2)
                
        return None
        
    def robust_click_element(self, locator, timeout=30, max_attempts=3):
        """Click element with retry mechanism and multiple strategies."""
        for attempt in range(max_attempts):
            try:
                element = self.robust_find_element(locator, timeout)
                
                # Strategy 1: Regular click
                try:
                    element.click()
                    if self.logger:
                        self.logger.info(f"Successfully clicked element {locator}")
                    return True
                except ElementNotInteractableException:
                    # Strategy 2: JavaScript click
                    if self.logger:
                        self.logger.info(f"Regular click failed, trying JavaScript click for {locator}")
                    self.browser.execute_script("arguments[0].click();", element)
                    return True
                    
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Click attempt {attempt + 1} failed for {locator}: {str(e)}")
                if attempt == max_attempts - 1:
                    raise
                time.sleep(2)
                
        return False
        
    def wait_for_page_stable(self, timeout=30):
        """Wait for page to be stable (no pending requests, DOM ready)."""
        try:
            # Wait for document ready state
            WebDriverWait(self.browser, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for jQuery if present
            try:
                WebDriverWait(self.browser, 5).until(
                    lambda d: d.execute_script("return typeof jQuery === 'undefined' || jQuery.active === 0")
                )
            except:
                pass  # jQuery might not be present
                
            # Additional wait for any animations/transitions
            time.sleep(1)
            
            if self.logger:
                self.logger.info("Page is stable and ready")
                
        except TimeoutException:
            if self.logger:
                self.logger.warning("Page stability check timed out, proceeding anyway")
                
    def robust_send_keys(self, locator, text, timeout=30, clear_first=True):
        """Send keys to element with robust error handling."""
        element = self.robust_find_element(locator, timeout)
        
        if clear_first:
            try:
                element.clear()
            except:
                # If clear fails, try JavaScript
                self.browser.execute_script("arguments[0].value = '';", element)
                
        try:
            element.send_keys(text)
        except ElementNotInteractableException:
            # Fallback to JavaScript
            self.browser.execute_script("arguments[0].value = arguments[1];", element, text)
            
        if self.logger:
            self.logger.info(f"Successfully sent keys to {locator}")
            
    def take_debug_screenshot(self, name="debug"):
        """Take screenshot for debugging purposes."""
        try:
            filename = f"/tmp/{name}_{int(time.time())}.png"
            self.browser.save_screenshot(filename)
            if self.logger:
                self.logger.info(f"Debug screenshot saved: {filename}")
            return filename
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to take screenshot: {str(e)}")
            return None