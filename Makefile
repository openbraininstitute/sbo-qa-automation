# Common test command template
TEST_CMD = uv run pytest $(TEST) --env=$(ENV) --env_url=$(ENV_URL) --browser-name=firefox $(HEADLESS) -sv

# Default variables
ENV ?= production
ENV_URL ?= production
HEADLESS ?=


setup:
	uv install --upgrade
	uv lint
	@echo "Environment setup complete. Use 'uv' commands to run tests and linting."


production:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_*.py --html=report.html --self-contained-html"

staging:
	$(MAKE) run-tests ENV=staging ENV_URL=staging TEST="tests/test_*.py --html=report.html --self-contained-html"

smoke:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_build_synaptome.py tests/test_about.py --html=report.html --self-contained-html"

smoke-staging:
	$(MAKE) run-tests ENV=staging ENV_URL=staging TEST="tests/test_build_synaptome.py tests/test_about.py --html=report.html --self-contained-html"

regression:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_*.py --html=report.html --self-contained-html"

feature:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_explore_emodel.py tests/test_morphology.py --html=report.html --self-contained-html"

feature-staging:
	$(MAKE) run-tests ENV=staging ENV_URL=staging TEST="tests/test_explore_emodel.py --html=report.html --self-contained-html"

# Main test runner
run-tests:
	@echo "Running tests in environment: $(ENV)"
	$(TEST_CMD)

# Help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  setup        Install environment dependencies."
	@echo "  production   Run all tests in the production environment."
	@echo "  staging      Run all tests in the staging environment."
	@echo "  smoke        Run smoke tests (basic group) in production."
	@echo "  smoke-staging Run smoke tests (basic group) in staging."
	@echo "  regression   Run full regression suite."
	@echo "  feature      Run feature-specific tests."
	@echo "  run-tests    Run a specific test or test pattern. Specify TEST, ENV, etc."

