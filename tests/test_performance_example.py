# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
"""
Example test demonstrating performance tracking across multiple pages.
"""
import pytest
from util.performance_tracker import PerformanceTracker


@pytest.mark.performance
class TestPerformanceTracking:
    """Example tests showing how to measure page performance."""
    
    def test_measure_public_pages_performance(self, visit_public_pages, logger):
        """Measure performance of public pages."""
        visit, base_url = visit_public_pages
        browser, wait = visit("")
        
        # Initialize performance tracker
        perf_tracker = PerformanceTracker(browser, logger)
        
        # Measure landing page
        perf_tracker.capture_metrics("Landing Page")
        
        # Measure about page
        browser, wait = visit("about")
        perf_tracker.capture_metrics("About Page")
        
        # Measure mission page
        browser, wait = visit("mission")
        perf_tracker.capture_metrics("Mission Page")
        
        # Measure news page
        browser, wait = visit("news")
        perf_tracker.capture_metrics("News Page")
        
        # Save report
        perf_tracker.save_report("performance_public_pages.json")
        
        # Get summary
        summary = perf_tracker.get_summary()
        logger.info(f"\nPerformance Summary:")
        logger.info(f"Pages measured: {summary['total_pages_measured']}")
        logger.info(f"Average load time: {summary['average_load_time']:.2f}ms")
        logger.info(f"Slowest page: {summary['slowest_page']}")
        
        # Optional: Assert performance thresholds
        assert summary['average_load_time'] < 5000, "Average load time exceeds 5 seconds"
    
    def test_measure_authenticated_pages_performance(self, login_direct_complete, logger, test_config):
        """Measure performance of authenticated pages."""
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        
        perf_tracker = PerformanceTracker(browser, logger)
        
        # Note: Skip measuring the initial login page as it's already loaded
        # and timing data may be stale
        
        # Measure project home page
        project_url = f"{base_url}/app/virtual-lab/lab/{lab_id}/project/{project_id}/home"
        logger.info(f"Navigating to: {project_url}")
        browser.get(project_url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        perf_tracker.capture_metrics("Project Home")
        
        # Measure notebooks page
        notebooks_url = f"{base_url}/app/virtual-lab/{lab_id}/{project_id}/notebooks/public"
        logger.info(f"Navigating to: {notebooks_url}")
        browser.get(notebooks_url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        perf_tracker.capture_metrics("Notebooks Page")
        
        # Measure data page
        data_url = f"{base_url}/app/virtual-lab/{lab_id}/{project_id}/data"
        logger.info(f"Navigating to: {data_url}")
        browser.get(data_url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        perf_tracker.capture_metrics("Data Page")
        
        # Save report
        perf_tracker.save_report("performance_authenticated_pages.json")
        
        summary = perf_tracker.get_summary()
        logger.info(f"\nAuthenticated Pages Performance Summary:")
        logger.info(f"Pages measured: {summary['total_pages_measured']}")
        logger.info(f"Average load time: {summary['average_load_time']:.2f}ms")
        logger.info(f"Slowest page: {summary['slowest_page']}")
        
        # Optional: Assert performance thresholds
        assert summary['average_load_time'] < 5000, "Average load time exceeds 5 seconds"

    def test_measure_login_flow_performance(self, public_browsing, logger, test_config):
        """Measure performance of login flow including redirects."""
        import time
        import os
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        
        browser, wait, base_url = public_browsing
        perf_tracker = PerformanceTracker(browser, logger)
        
        # Navigate to landing page first
        logger.info(f"Navigating to landing page: {base_url}")
        browser.get(base_url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(1)  # Let timing API populate
        
        # Measure landing page
        logger.info("Measuring landing page performance")
        perf_tracker.capture_metrics("Landing Page")
        
        # Click "Go to Lab" button and measure redirect
        logger.info("Clicking 'Go to Lab' button")
        start_time = time.time()
        
        try:
            login_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='/app/virtual-lab']"))
            )
            login_btn.click()
        except:
            logger.warning("Could not find login button, trying alternative selector")
            login_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'virtual-lab')]"))
            )
            login_btn.click()
        
        # Wait for redirect to login page
        wait.until(EC.url_contains("openid-connect"))
        redirect_time = (time.time() - start_time) * 1000  # Convert to ms
        logger.info(f"Redirect to login page took: {redirect_time:.2f}ms")
        
        # Measure login page load
        time.sleep(1)  # Let timing API populate
        perf_tracker.capture_metrics("Login Page (Keycloak)")
        
        # Perform login and measure
        logger.info("Performing login")
        username = test_config.get("username")
        password = test_config.get("password") or os.getenv("OBI_PASSWORD")
        
        start_login = time.time()
        
        # Enter credentials using JavaScript (more reliable)
        browser.execute_script(f"""
            document.getElementById('username').value = '{username}';
            document.getElementById('username').dispatchEvent(new Event('input', {{ bubbles: true }}));
        """)
        
        browser.execute_script(f"""
            document.getElementById('password').value = arguments[0];
            document.getElementById('password').dispatchEvent(new Event('input', {{ bubbles: true }}));
        """, password)
        
        # Click login
        login_submit = browser.find_element(By.ID, "kc-login")
        browser.execute_script("arguments[0].click();", login_submit)
        
        # Wait for login to complete
        wait.until(lambda d: "virtual-lab" in d.current_url or "sync" in d.current_url)
        login_time = (time.time() - start_login) * 1000
        logger.info(f"Login and redirect took: {login_time:.2f}ms")
        
        # Measure post-login page
        time.sleep(1)
        perf_tracker.capture_metrics("Virtual Lab (After Login)")
        
        # Add custom metrics for redirects
        from datetime import datetime
        perf_tracker.metrics.append({
            'page_name': 'Landing → Login Redirect',
            'url': 'redirect',
            'timestamp': datetime.now().isoformat(),
            'total_time': int(redirect_time),
            'dns_lookup_time': 0,
            'tcp_connection_time': 0,
            'request_time': 0,
            'response_time': 0,
            'dom_processing_time': 0,
            'dom_interactive_time': 0,
            'dom_content_loaded_time': 0,
            'page_load_time': int(redirect_time),
            'redirect_count': 1
        })
        
        perf_tracker.metrics.append({
            'page_name': 'Login → Virtual Lab Redirect',
            'url': 'redirect',
            'timestamp': datetime.now().isoformat(),
            'total_time': int(login_time),
            'dns_lookup_time': 0,
            'tcp_connection_time': 0,
            'request_time': 0,
            'response_time': 0,
            'dom_processing_time': 0,
            'dom_interactive_time': 0,
            'dom_content_loaded_time': 0,
            'page_load_time': int(login_time),
            'redirect_count': 1
        })
        
        # Save report
        perf_tracker.save_report("performance_login_flow.json")
        
        summary = perf_tracker.get_summary()
        logger.info(f"\nLogin Flow Performance Summary:")
        logger.info(f"Pages measured: {summary['total_pages_measured']}")
        logger.info(f"Average load time: {summary['average_load_time']:.2f}ms")
        logger.info(f"Landing → Login redirect: {redirect_time:.2f}ms")
        logger.info(f"Login → Virtual Lab: {login_time:.2f}ms")
        logger.info(f"Total login flow time: {redirect_time + login_time:.2f}ms")
        
        # Assert reasonable login flow time
        total_flow_time = redirect_time + login_time
        assert total_flow_time < 10000, f"Login flow too slow: {total_flow_time:.2f}ms"
