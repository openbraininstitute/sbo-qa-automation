# Test Generation and Performance Tracking Guide

## 1. Performance Tracking

### Quick Start
Measure page load times and performance metrics:

```python
from util.performance_tracker import PerformanceTracker

def test_my_page_performance(self, public_browsing, logger):
    browser, wait, base_url = public_browsing
    
    # Initialize tracker
    perf_tracker = PerformanceTracker(browser, logger)
    
    # Navigate and measure
    browser.get(f"{base_url}/about")
    perf_tracker.capture_metrics("About Page")
    
    # Save report
    perf_tracker.save_report("my_performance_report.json")
```

### Run Performance Tests
```bash
# Run the example performance test
make run-tests TEST="tests/test_performance_example.py" ENV=staging

# View the generated report
cat performance_public_pages.json
```

### Metrics Captured
- **DNS Lookup Time**: Time to resolve domain name
- **TCP Connection Time**: Time to establish connection
- **Request Time**: Time from request sent to first byte received
- **Response Time**: Time to download response
- **DOM Processing Time**: Time to parse and process DOM
- **DOM Interactive Time**: Time until DOM is interactive
- **DOM Content Loaded**: Time until DOMContentLoaded event
- **Total Page Load Time**: Complete page load time

### Performance Thresholds
Add assertions to fail tests if pages are too slow:

```python
summary = perf_tracker.get_summary()
assert summary['average_load_time'] < 3000, "Pages too slow (>3s average)"
assert summary['max_load_time'] < 5000, "Slowest page exceeds 5s"
```

## 2. Recording Tests from User Interactions

### Interactive Recording
Record your clicks and inputs to generate test code automatically:

```bash
# Start recording
python record_test.py --test-name "explore_workflow" --env staging

# The browser will open - perform your test actions
# Press ENTER when done

# Generated test will be saved to tests/test_explore_workflow.py
```

### Options
```bash
# Record with custom output file
python record_test.py --test-name "my_test" --output tests/test_custom.py

# Record starting from specific URL
python record_test.py --test-name "my_test" --start-url "https://example.com/page"

# Record in headless mode (no browser window)
python record_test.py --test-name "my_test" --headless
```

### What Gets Recorded
- ✅ Button clicks
- ✅ Link clicks
- ✅ Form inputs (text, email, etc.)
- ✅ Password fields (masked in output)
- ✅ Element selectors (ID, class, name)

### Generated Code Example
```python
# Auto-generated test code
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TestExploreWorkflow:
    def test_explore_workflow(self, login_direct_complete, logger):
        browser, wait, base_url, lab_id, project_id = login_direct_complete
        
        # Click: Explore
        element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.nav-link'))
        )
        element.click()
        logger.info('Clicked element: Explore')
        
        # Add assertions here
        assert browser.current_url, 'Page should be loaded'
```

### Post-Recording Steps
1. **Review the generated code** - The recorder captures raw interactions
2. **Add assertions** - Verify expected outcomes
3. **Add waits** - Ensure elements are ready before interaction
4. **Refactor** - Extract common patterns into page objects
5. **Test it** - Run the generated test to verify it works

## 3. Manual Test Creation

### Using Page Objects
Create maintainable tests using the page object pattern:

```python
from pages.landing_page import LandingPage

def test_landing_page_navigation(self, public_browsing, logger):
    browser, wait, base_url = public_browsing
    landing_page = LandingPage(browser, wait, base_url, logger)
    
    landing_page.go_to_landing_page()
    landing_page.click_about_link()
    
    assert "about" in browser.current_url
```

### Creating New Page Objects
```python
# pages/my_new_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class MyNewPage:
    def __init__(self, browser, wait, base_url, logger):
        self.browser = browser
        self.wait = wait
        self.base_url = base_url
        self.logger = logger
    
    # Locators
    SUBMIT_BUTTON = (By.ID, "submit-btn")
    TITLE_TEXT = (By.CSS_SELECTOR, "h1.title")
    
    def click_submit(self):
        element = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        element.click()
        self.logger.info("Clicked submit button")
    
    def get_title(self):
        element = self.wait.until(EC.presence_of_element_located(self.TITLE_TEXT))
        return element.text
```

## Best Practices

### Performance Testing
- Run performance tests regularly (daily/weekly)
- Track trends over time
- Set realistic thresholds based on your app
- Test from different locations/networks if possible
- Compare staging vs production performance

### Test Recording
- Record small, focused workflows
- One feature per recording session
- Review and refactor generated code
- Don't rely solely on recorded tests
- Use recordings as a starting point

### Test Maintenance
- Keep page objects up to date
- Use descriptive test names
- Add comments for complex interactions
- Group related tests in classes
- Use fixtures to reduce duplication

## Troubleshooting

### Performance Tracker Issues
```python
# If metrics are 0 or missing, ensure page is fully loaded
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
time.sleep(1)  # Give time for timing API to populate
perf_tracker.capture_metrics("Page Name")
```

### Recorder Issues
```python
# If actions aren't captured, manually trigger capture
recorder.capture_actions()  # Call periodically during recording

# If selectors are too complex, simplify by adding IDs/data-testid to elements
```

### Generated Test Issues
- **Flaky selectors**: Add data-testid attributes to your app
- **Timing issues**: Add explicit waits before interactions
- **Missing context**: Add setup/teardown in fixtures
