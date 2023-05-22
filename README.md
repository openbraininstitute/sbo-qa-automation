# UI Testing with Selenium Python Pytest - Page Object Model (POM)

## Features
- The tests use setup/teardown methods for the session. 
- Test with Chrom and Firefox (no additional configuration).
- Possibility to visually see the execution.
- Possibility to see the screenshots of the errors.
- A html report generated at each test run.

## Prerequisites
* Make sure pip is installed in your system.
* Install virtual environment.
* A json file with login credentials would need to be created.

### To activate the virtual environment:
```bash
source venv/bin/activate
```
## Run the tests
### To execute a test run this in your cmd: 
1. pytest tests -s -v

### To run tests and generate html/allure reporting and screenshots run this cmd:
 pytest --alluredir=allure_reports --html=report.html

### Accessing the reports and screenshots
* The screenshot of an error is in the 'screenshot' directory.
* The html reports are in the source directory.


