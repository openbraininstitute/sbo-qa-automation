# Performance Analysis Guide

## Quick Start

### 1. Run Performance Tests
```bash
# Test public pages
make run-tests TEST="tests/test_performance_example.py::TestPerformanceTracking::test_measure_public_pages_performance" ENV=staging

# Test authenticated pages
make run-tests TEST="tests/test_performance_example.py::TestPerformanceTracking::test_measure_authenticated_pages_performance" ENV=staging
```

This generates JSON files:
- `performance_public_pages.json`
- `performance_authenticated_pages.json`

### 2. View Results in Terminal
```bash
# Quick summary
python view_performance.py performance_public_pages.json

# Detailed metrics
python view_performance.py performance_public_pages.json --detailed

# Specific page breakdown
python view_performance.py performance_public_pages.json --breakdown "Landing Page"

# Compare multiple reports
python view_performance.py performance_*.json
```

### 3. Generate HTML Report
```bash
python generate_performance_html.py performance_public_pages.json
# Opens: performance_public_pages.html
```

Then open the HTML file in your browser for a visual report with charts and graphs.

## Understanding the Metrics

### Key Metrics Explained

| Metric | What It Measures | Good Value |
|--------|------------------|------------|
| **Total Time** | Complete page load time | < 3000ms |
| **DNS Lookup** | Time to resolve domain name | < 50ms |
| **TCP Connection** | Time to establish connection | < 100ms |
| **Request Time** | Time from request to first byte | < 500ms |
| **Response Time** | Time to download response | < 200ms |
| **DOM Processing** | Time to parse and process DOM | < 1000ms |
| **DOM Interactive** | Time until DOM is interactive | < 2000ms |
| **DOM Content Loaded** | Time until DOMContentLoaded event | < 2500ms |

### Performance Thresholds

- **Fast**: < 1000ms (green)
- **Acceptable**: 1000-3000ms (blue)
- **Slow**: > 3000ms (red)

## Analysis Workflows

### 1. Identify Slow Pages
```bash
# Find pages over 2 seconds
python view_performance.py performance_public_pages.json --threshold 2000
```

### 2. Compare Environments
```bash
# Run tests in both environments
make run-tests TEST="tests/test_performance_example.py" ENV=staging
# Save as: performance_staging.json

make run-tests TEST="tests/test_performance_example.py" ENV=production  
# Save as: performance_production.json

# Compare
python view_performance.py performance_staging.json performance_production.json
```

### 3. Track Performance Over Time
```bash
# Run tests daily and save with date
DATE=$(date +%Y%m%d)
make run-tests TEST="tests/test_performance_example.py" ENV=production
mv performance_public_pages.json performance_${DATE}.json

# Compare this week vs last week
python view_performance.py performance_20260114.json performance_20260107.json
```

### 4. Investigate Specific Issues

**Slow DNS Lookup (> 100ms)**
- Check DNS server configuration
- Consider using a CDN
- Verify network connectivity

**Slow Request Time (> 500ms)**
- Check server response time
- Look for database query issues
- Review API performance

**Slow DOM Processing (> 1000ms)**
- Reduce JavaScript bundle size
- Optimize CSS
- Minimize DOM complexity
- Check for render-blocking resources

## Integration with CI/CD

### Add Performance Tests to GitHub Actions

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Performance Tests
        run: |
          make run-tests TEST="tests/test_performance_example.py" ENV=production
      
      - name: Generate HTML Report
        run: |
          python generate_performance_html.py performance_public_pages.json
      
      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: performance-reports
          path: |
            performance_*.json
            performance_*.html
      
      - name: Check Thresholds
        run: |
          python view_performance.py performance_public_pages.json --threshold 3000
```

## Custom Performance Tests

### Add Performance Tracking to Existing Tests

```python
from util.performance_tracker import PerformanceTracker

def test_my_workflow(self, login_direct_complete, logger):
    browser, wait, base_url, lab_id, project_id = login_direct_complete
    
    # Initialize tracker
    perf = PerformanceTracker(browser, logger)
    
    # Your test actions
    browser.get(f"{base_url}/my-page")
    perf.capture_metrics("My Page")
    
    # More actions
    browser.get(f"{base_url}/another-page")
    perf.capture_metrics("Another Page")
    
    # Save report
    perf.save_report("my_workflow_performance.json")
    
    # Assert performance
    summary = perf.get_summary()
    assert summary['average_load_time'] < 3000, "Pages too slow"
```

## Troubleshooting

### Metrics Show 0 or Missing
```python
# Ensure page is fully loaded
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
time.sleep(1)  # Give time for timing API to populate
perf.capture_metrics("Page Name")
```

### Inconsistent Results
- Run tests multiple times and average
- Test at different times of day
- Consider network conditions
- Use headless mode for consistency

### High Variance
- Check for dynamic content loading
- Verify no background processes interfering
- Ensure stable network connection
- Run in CI/CD for consistent environment

## Best Practices

1. **Run regularly** - Daily or weekly to track trends
2. **Set baselines** - Know your normal performance
3. **Alert on regressions** - Fail tests if performance degrades
4. **Test realistic scenarios** - Use actual user workflows
5. **Compare environments** - Staging vs production
6. **Document findings** - Keep notes on performance issues
7. **Share reports** - Make HTML reports available to team

## Example: Weekly Performance Review

```bash
#!/bin/bash
# weekly_performance_check.sh

DATE=$(date +%Y%m%d)

# Run tests
make run-tests TEST="tests/test_performance_example.py" ENV=production

# Generate reports
python generate_performance_html.py performance_public_pages.json performance_${DATE}.html
python view_performance.py performance_public_pages.json > performance_${DATE}.txt

# Email or post to Slack
# mail -s "Weekly Performance Report" team@example.com < performance_${DATE}.txt
```

Run weekly:
```bash
chmod +x weekly_performance_check.sh
# Add to crontab: 0 9 * * 1 /path/to/weekly_performance_check.sh
```
