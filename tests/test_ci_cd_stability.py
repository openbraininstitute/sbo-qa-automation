# Copyright (c) 2024 Blue Brain Project/EPFL
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0

import pytest
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestCICDStability:
    """Test cases specifically designed to validate CI/CD stability and identify environment-specific issues."""
    
    @pytest.mark.smoke
    def test_browser_initialization(self, setup, logger):
        """Test that browser initializes correctly in CI/CD environment."""
        browser, wait, base_url, lab_id, project_id = setup
        
        # Test basic browser functionality
        assert browser is not None, "Browser should be initialized"
        assert wait is not None, "WebDriverWait should be initialized"
        
        # Test window size (important for headless mode)
        size = browser.get_window_size()
        logger.info(f"Browser window size: {size}")
        assert size['width'] >= 1400, f"Window width should be at least 1400, got {size['width']}"
        # More flexible height check for different environments
        assert size['height'] >= 900, f"Window height should be at least 900, got {size['height']}"
        
        # Test basic navigation
        browser.get("https://www.google.com")
        assert "google" in browser.current_url.lower(), "Should be able to navigate to Google"
        
        logger.info("✅ Browser initialization test passed")

    @pytest.mark.smoke
    def test_login_stability(self, setup, navigate_to_login_direct, test_config, logger):
        """Test login process stability with enhanced error handling."""
        login_page = navigate_to_login_direct
        username = test_config["username"]
        password = os.getenv("OBI_PASSWORD")
        
        logger.info(f"Testing login with username: {username[:3]}***")
        
        # Test login with retry mechanism
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                logger.info(f"Login attempt {attempt + 1}/{max_attempts}")
                login_page.perform_login(username, password)
                login_page.wait_for_login_complete(timeout=90)
                logger.info("✅ Login successful")
                break
            except TimeoutException as e:
                logger.warning(f"Login attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_attempts - 1:
                    # Final attempt failed, capture debug info
                    logger.error(f"All login attempts failed. Final URL: {login_page.browser.current_url}")
                    login_page.browser.save_screenshot("/tmp/login_failure.png")
                    raise
                else:
                    # Wait before retry
                    time.sleep(5)
                    
        browser, wait, base_url, lab_id, project_id = setup
        
        # Verify we're actually logged in
        current_url = browser.current_url
        assert any(keyword in current_url for keyword in ["virtual-lab", "sync", "app"]), \
            f"Should be redirected to app after login. Current URL: {current_url}"
            
        logger.info("✅ Login stability test passed")

    @pytest.mark.smoke  
    def test_page_load_performance(self, public_browsing, logger):
        """Test page load performance to identify slow loading issues in CI/CD."""
        browser, wait, base_url = public_browsing
        
        test_pages = [
            "/",
            "/about", 
            "/mission",
            "/news"
        ]
        
        performance_results = {}
        
        for page in test_pages:
            start_time = time.time()
            try:
                url = f"{base_url}{page}"
                logger.info(f"Loading page: {url}")
                browser.get(url)
                
                # Wait for page to be ready
                wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
                
                load_time = time.time() - start_time
                performance_results[page] = load_time
                logger.info(f"Page {page} loaded in {load_time:.2f} seconds")
                
                # Assert reasonable load time (adjust threshold as needed)
                assert load_time < 30, f"Page {page} took too long to load: {load_time:.2f}s"
                
            except TimeoutException:
                load_time = time.time() - start_time
                logger.error(f"Page {page} failed to load within timeout. Time elapsed: {load_time:.2f}s")
                raise
                
        # Log performance summary
        avg_load_time = sum(performance_results.values()) / len(performance_results)
        logger.info(f"Average page load time: {avg_load_time:.2f} seconds")
        logger.info(f"Performance results: {performance_results}")
        
        logger.info("✅ Page load performance test passed")

    @pytest.mark.smoke
    def test_element_interaction_stability(self, navigate_to_landing_page, logger):
        """Test element interaction stability in headless mode."""
        landing_page = navigate_to_landing_page
        
        # Test basic element interactions that commonly fail in headless mode
        try:
            # Test clicking elements
            go_to_lab_btn = landing_page.go_to_lab()
            assert go_to_lab_btn.is_displayed(), "Go to Lab button should be visible"
            
            # Test scrolling (important for headless mode)
            landing_page.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            landing_page.browser.execute_script("window.scrollTo(0, 0);")
            
            # Test element visibility after scroll
            go_to_lab_btn = landing_page.go_to_lab()
            assert go_to_lab_btn.is_displayed(), "Button should still be visible after scroll"
            
            logger.info("✅ Element interaction stability test passed")
            
        except Exception as e:
            logger.error(f"Element interaction failed: {str(e)}")
            landing_page.browser.save_screenshot("/tmp/interaction_failure.png")
            raise

import os