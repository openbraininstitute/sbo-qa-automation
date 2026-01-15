# UI Tests with Selenium Python Pytest

## Overview
Comprehensive test automation framework for the Open Brain Institute platform using Selenium, Python, and Pytest. Includes functional tests, performance monitoring, and test generation tools.

## Features
- **Functional Testing** - Setup/teardown methods, Chrome and Firefox support (headless mode available)
- **Visual Debugging** - See test execution in real-time, automatic screenshots on failures
- **HTML Reports** - Detailed test reports generated for each run
- **Performance Tracking** - Measure page load times, DOM processing, and network metrics
- **Test Recording** - Auto-generate test code from user interactions
- **Page Object Model** - Maintainable test structure with separate locators, pages, and tests
- **CI/CD Integration** - GitHub Actions workflows for automated testing
- **Easy Sharing** - Share tests via Git, Docker, or CI/CD pipelines

## Quick Start

### Prerequisites
- Python 3.11+
- pip package manager
- uv (recommended) or virtualenv

### Installation

1. **Install uv** (recommended):
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# macOS with Homebrew
brew install uv

# Cross-platform with pip
pip install uv
```

2. **Create virtual environment**:
```bash
# Using uv (recommended)
uv venv -p 3.11
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt
```

3. **Set environment variables**:
```bash
export OBI_USERNAME="your-username"
export OBI_PASSWORD="your-password"
export LAB_ID_STAGING="your-lab-id"
export PROJECT_ID_STAGING="your-project-id"
export LAB_ID_PRODUCTION="your-lab-id"
export PROJECT_ID_PRODUCTION="your-project-id"
```

### Running Tests

```bash
# Run all tests in staging
make staging

# Run all tests in production
make production

# Run smoke tests (core functionality)
make smoke-staging

# Run performance tests
make performance

# Run specific test file
make run-tests TEST="tests/test_landing.py" ENV=staging

# Run in headless mode
make run-tests TEST="tests/test_*.py" ENV=staging HEADLESS="--headless"
```

## Available Make Targets

| Command | Description |
|---------|-------------|
| `make setup` | Install dependencies and setup environment |
| `make production` | Run all tests in production |
| `make staging` | Run all tests in staging |
| `make smoke` | Run smoke tests in production |
| `make smoke-staging` | Run smoke tests in staging |
| `make performance` | Run performance tests in staging |
| `make performance-production` | Run performance tests in production |
| `make regression` | Run full regression suite |
| `make feature` | Run feature-specific tests |
| `make help` | Show all available targets |

## Performance Testing

### Run Performance Tests
```bash
# Run all performance tests
make performance

# View results in terminal
python view_performance.py performance_*.json

# Generate HTML reports
python generate_performance_html.py performance_public_pages.json
python generate_performance_html.py performance_authenticated_pages.json
python generate_performance_html.py performance_login_flow.json

# Open reports in browser
open performance_*.html
```

### Performance Metrics Tracked
- Total page load time
- DNS lookup time
- TCP connection time
- Request/response time
- DOM processing time
- DOM interactive time
- DOM content loaded time

See [PERFORMANCE_ANALYSIS.md](PERFORMANCE_ANALYSIS.md) for detailed guide.

## Test Recording

Record user interactions to auto-generate test code:

```bash
# Record from landing page
python record_test.py --test-name "my_test" --env staging

# Record from authenticated page (auto-login)
python record_test.py --test-name "notebook_test" --start-page notebooks --env staging

# Record with custom URL
python record_test.py --test-name "custom" --start-url "https://example.com/page"
```

**Note**: Generated tests are starting points and need manual refinement. See [RECORDER_LIMITATIONS.md](RECORDER_LIMITATIONS.md) for details.

## Project Structure

```
sbo-qa-automation/
├── tests/              # Test files
├── pages/              # Page object classes
├── locators/           # Element locators
├── util/               # Utility modules (performance tracker, test recorder)
├── data/               # Test data
├── conftest.py         # Pytest fixtures and configuration
├── pytest.ini          # Pytest settings
├── Makefile            # Command shortcuts
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Test Coverage

### Public Pages
- Landing page (titles, navigation, logos)
- About page
- Mission page
- News page

### Authenticated Pages
- Virtual lab home
- Project home
- Notebooks page
- Data page

### Explore Page
- Experimental data types display
- Model data display
- Brain region search
- 3D Atlas interaction
- Morphology, Electrophysiology, Neuron density tabs

### Functional Tests
- Login/logout flows
- Navigation between pages
- Form interactions
- Data filtering and search
- Table operations
- Detail view verification

## Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick command reference
- **[TEST_GENERATION_GUIDE.md](TEST_GENERATION_GUIDE.md)** - Performance tracking and test recording guide
- **[PERFORMANCE_ANALYSIS.md](PERFORMANCE_ANALYSIS.md)** - Analyzing performance test results
- **[RECORDER_LIMITATIONS.md](RECORDER_LIMITATIONS.md)** - Test recorder best practices
- **[SHARING_TESTS.md](SHARING_TESTS.md)** - How to share tests with colleagues

## Test Reports

### HTML Reports
Generated automatically after each test run:
- `report.html` - Main test report
- `performance_*.html` - Performance reports

### Screenshots
Failed test screenshots saved to:
- `latest_logs/errors/` - Error screenshots with test names

### Logs
- `allure_reports/report.log` - Detailed test execution logs

## CI/CD Integration

Tests run automatically via GitHub Actions:
- On pull requests
- On push to main branch
- Scheduled daily runs
- Manual workflow dispatch

See `.github/workflows/` for workflow configurations.

## Forked Repositories

If you've forked this repository, sync with upstream:

```bash
git remote add upstream git@github.com:openbraininstitute/sbo-qa-automation.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Troubleshooting

### Common Issues

**Tests fail with "element not found"**
- Check if selectors have changed in the UI
- Update locators in `locators/` directory
- Add explicit waits if needed

**Performance metrics show 0 or negative values**
- Ensure page is fully loaded before capturing metrics
- Add `time.sleep(1)` after page load
- Check browser console for JavaScript errors

**Login tests fail**
- Verify environment variables are set
- Check credentials are correct
- Ensure network connectivity to auth server

**Headless mode issues**
- Some tests may behave differently in headless mode
- Try running without `--headless` flag first
- Check window size settings in conftest.py

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests locally: `make smoke-staging`
4. Update documentation if needed
5. Submit a pull request

## Best Practices

1. **Use Page Object Model** - Keep locators, pages, and tests separate
2. **Add data-testid attributes** - Makes selectors more stable
3. **Write meaningful assertions** - Don't just check page loaded
4. **Add logging** - Help debug when tests fail
5. **Run performance tests regularly** - Track performance trends
6. **Keep tests independent** - Each test should run standalone
7. **Use fixtures** - Reduce code duplication

## Support

For issues or questions:
- Check documentation in this repository
- Review existing test examples
- Contact the QA team

## Acknowledgment

The development of this software was supported by funding to the Blue Brain Project, 
a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government's ETH Board of the Swiss Federal Institutes of Technology.

Copyright © 2024 Blue Brain Project/EPFL

Copyright © 2025 Open Brain Institute
