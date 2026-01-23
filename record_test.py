#!/usr/bin/env env python
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
"""
Interactive test recorder script.
Run this to record user interactions and generate test code.

Usage:
    python record_test.py --test-name "My Test" --env staging
"""
import argparse
import logging
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

from util.test_recorder import TestRecorder


def perform_login(browser, wait, username, password, logger, env):
    """Perform login to the application."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Determine base URL
        if env == 'staging':
            base_url = 'https://staging.openbraininstitute.org'
        else:
            base_url = 'https://www.openbraininstitute.org'
        
        # Navigate to landing page
        logger.info(f"Navigating to {base_url}")
        browser.get(base_url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(1)
        
        # Click "Go to Lab" button
        logger.info("Looking for login button...")
        login_selectors = [
            (By.XPATH, "//a[@href='/app/virtual-lab']"),
            (By.XPATH, "//a[contains(@href, 'virtual-lab')]"),
            (By.CSS_SELECTOR, "[href*='virtual-lab']"),
        ]
        
        login_clicked = False
        for selector in login_selectors:
            try:
                login_btn = wait.until(EC.element_to_be_clickable(selector))
                logger.info(f"Found login button with selector: {selector}")
                login_btn.click()
                login_clicked = True
                break
            except:
                continue
        
        if not login_clicked:
            logger.error("Could not find login button")
            raise RuntimeError("Login button not found")
        
        # Wait for redirect to login page
        logger.info("Waiting for login page...")
        wait.until(EC.url_contains("openid-connect"))
        time.sleep(2)
        
        # Wait for login form to be visible
        wait.until(EC.presence_of_element_located((By.ID, "kc-form-wrapper")))
        time.sleep(1)
        
        # Enter username using JavaScript
        logger.info("Entering username...")
        browser.execute_script(f"""
            document.getElementById('username').value = '{username}';
            document.getElementById('username').dispatchEvent(new Event('input', {{ bubbles: true }}));
        """)
        time.sleep(0.5)
        
        # Enter password using JavaScript
        logger.info("Entering password...")
        browser.execute_script(f"""
            document.getElementById('password').value = arguments[0];
            document.getElementById('password').dispatchEvent(new Event('input', {{ bubbles: true }}));
        """, password)
        time.sleep(0.5)
        
        # Click login button
        logger.info("Clicking login button...")
        login_submit = browser.find_element(By.ID, "kc-login")
        browser.execute_script("arguments[0].click();", login_submit)
        
        # Wait for login to complete
        logger.info("Waiting for login to complete...")
        wait.until(lambda d: "virtual-lab" in d.current_url or "sync" in d.current_url, 
                  message="Login did not complete")
        
        # Give the app time to fully load
        time.sleep(3)
        
        logger.info("✅ Login successful!")
        
    except Exception as e:
        logger.error(f"Login failed: {e}")
        logger.error(f"Current URL: {browser.current_url}")
        browser.save_screenshot("/tmp/login_failed.png")
        raise


def setup_logger():
    """Setup logging for the recorder."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(handler)
    return logger


def create_browser(headless=False):
    """Create a browser instance for recording."""
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    
    browser = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=options
    )
    browser.set_window_size(1400, 900)
    wait = WebDriverWait(browser, 30)
    return browser, wait


def main():
    parser = argparse.ArgumentParser(description='Record user interactions and generate test code')
    parser.add_argument('--test-name', required=True, help='Name for the generated test')
    parser.add_argument('--env', choices=['staging', 'production'], default='staging',
                       help='Environment to test against')
    parser.add_argument('--start-url', help='Starting URL (optional, defaults to env base URL)')
    parser.add_argument('--start-page', choices=['landing', 'lab', 'project', 'notebooks'],
                       help='Starting page type (uses env variables for IDs)')
    parser.add_argument('--login', action='store_true', help='Perform login before recording')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    logger = setup_logger()
    
    # Get credentials if login is needed
    username = os.getenv("OBI_USERNAME")
    password = os.getenv("OBI_PASSWORD")
    
    # Determine if we need to login
    needs_login = args.login or args.start_page in ['lab', 'project', 'notebooks']
    
    if needs_login and (not username or not password):
        logger.error("OBI_USERNAME and OBI_PASSWORD environment variables required for login")
        sys.exit(1)
    
    # Determine base URL
    if args.start_url:
        start_url = args.start_url
    elif args.start_page:
        # Build URL from environment variables
        if args.env == 'staging':
            base_url = 'https://dev.openbraininstitute.org'
            lab_id = os.getenv('LAB_ID_STAGING')
            project_id = os.getenv('PROJECT_ID_STAGING')
        else:
            base_url = 'https://www.openbraininstitute.org'
            lab_id = os.getenv('LAB_ID_PRODUCTION')
            project_id = os.getenv('PROJECT_ID_PRODUCTION')
        
        if args.start_page == 'landing':
            start_url = base_url
        elif args.start_page == 'lab':
            start_url = f"{base_url}/app/virtual-lab"
        elif args.start_page == 'project':
            if not lab_id or not project_id:
                logger.error("LAB_ID and PROJECT_ID environment variables required for project page")
                sys.exit(1)
            start_url = f"{base_url}/app/virtual-lab/lab/{lab_id}/project/{project_id}/home"
        elif args.start_page == 'notebooks':
            if not lab_id or not project_id:
                logger.error("LAB_ID and PROJECT_ID environment variables required for notebooks page")
                sys.exit(1)
            start_url = f"{base_url}/app/virtual-lab/{lab_id}/{project_id}/notebooks/public"
    elif args.env == 'staging':
        start_url = 'https://dev.openbraininstitute.org'
    else:
        start_url = 'https://www.openbraininstitute.org'
    
    logger.info(f"Starting test recorder for: {args.test_name}")
    logger.info(f"Environment: {args.env}")
    logger.info(f"Starting URL: {start_url}")
    
    # Create browser
    browser, wait = create_browser(args.headless)
    
    try:
        # Initialize recorder
        recorder = TestRecorder(browser, logger)
        
        # Handle login if needed
        if needs_login:
            logger.info("Performing login...")
            perform_login(browser, wait, username, password, logger, args.env)
        
        # Navigate to starting URL
        logger.info(f"Navigating to {start_url}")
        browser.get(start_url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        
        # Give page time to fully load
        time.sleep(2)
        
        # Start recording
        recorder.start_recording(args.test_name)
        
        logger.info("\n" + "="*60)
        logger.info("RECORDING STARTED")
        logger.info("="*60)
        logger.info("Perform your test actions in the browser window.")
        logger.info("Press ENTER in this terminal when done recording...")
        logger.info("="*60 + "\n")
        
        # Wait for user to finish
        input()
        
        # Capture final actions
        recorder.capture_actions()
        
        # Stop recording
        actions = recorder.stop_recording()
        
        logger.info(f"\nRecorded {len(actions)} actions")
        
        # Generate and save test code
        if args.output:
            output_file = args.output
        else:
            output_file = f"tests/test_{args.test_name.lower().replace(' ', '_')}.py"
        
        recorder.save_test_file(output_file)
        recorder.save_actions_json()
        
        logger.info("\n" + "="*60)
        logger.info("RECORDING COMPLETE")
        logger.info("="*60)
        logger.info(f"Test code saved to: {output_file}")
        logger.info("Review and edit the generated code before running.")
        logger.info("="*60 + "\n")
        
    except KeyboardInterrupt:
        logger.info("\nRecording cancelled by user")
    except Exception as e:
        logger.error(f"Error during recording: {e}")
        raise
    finally:
        browser.quit()


if __name__ == '__main__':
    main()
