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
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_about.py \
            tests/test_mission.py \
            tests/test_news.py \
            tests/test_landing.py \
            tests/test_login.py \
            tests/test_explore_page.py \
            tests/test_project_home.py \
            tests/test_project_notebooks.py \
            tests/test_explore_emodel.py \
			tests/test_ai_assistant_workflow.py \
			tests/test_build_single_neuron.py \
			tests/test_digital_brain_story.py \
			tests/test_team.py \
			tests/test_contact.py \
			tests/test_explore_ephys.py \
            -sv \
            --html=report.html --self-contained-html"

smoke-staging:
	$(MAKE) run-tests ENV=staging ENV_URL=staging TEST="tests/test_landing.py \
            tests/test_about.py \
            tests/test_mission.py \
            tests/test_news.py \
            tests/test_login.py \
            tests/test_explore_page.py \
            tests/test_project_home.py \
            tests/test_project_notebooks.py \
            tests/test_explore_emodel.py \
			tests/test_ai_assistant_workflow.py \
			tests/test_build_single_neuron.py \
			tests/test_digital_brain_story.py \
			tests/test_team.py \
			tests/test_contact.py \
			tests/test_explore_ephys.py \
            --html=report.html --self-contained-html"

# New CI/CD stability tests
ci-cd-stability:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_ci_cd_stability.py --html=report.html --self-contained-html"

ci-cd-stability-headless:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_ci_cd_stability.py --html=report.html --self-contained-html" HEADLESS="--headless"

# Performance tests
performance:
	$(MAKE) run-tests ENV=staging ENV_URL=staging TEST="tests/test_performance_example.py --html=report.html --self-contained-html"
	@echo "\n📊 Performance reports generated:"
	@echo "  - performance_public_pages.json"
	@echo "  - performance_authenticated_pages.json"
	@echo "  - performance_login_flow.json"
	@echo "\nView reports:"
	@echo "  python view_performance.py performance_*.json"
	@echo "  python generate_performance_html.py performance_public_pages.json"

performance-production:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_performance_example.py --html=report.html --self-contained-html"

regression:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_*.py --html=report.html --self-contained-html"

feature:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_explore_emodel.py -vs --html=report.html --self-contained-html"

feature-staging:
	$(MAKE) run-tests ENV=staging ENV_URL=staging TEST="tests/test_explore_emodel.py --html=report.html --self-contained-html"

# Debug failing tests
debug-explore:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_explore_page.py --html=report.html --self-contained-html --tb=long -vvv"

debug-explore-headless:
	$(MAKE) run-tests ENV=production ENV_URL=production TEST="tests/test_explore_page.py --html=report.html --self-contained-html --tb=long" HEADLESS="--headless"

# Main test runner
run-tests:
	@echo "Running tests in environment: $(ENV)"
	$(TEST_CMD)

# Help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  setup                Install environment dependencies."
	@echo "  production           Run all tests in the production environment."
	@echo "  staging              Run all tests in the staging environment."
	@echo "  smoke                Run smoke tests (basic group) in production."
	@echo "  smoke-staging        Run smoke tests (basic group) in staging."
	@echo "  ci-cd-stability      Run CI/CD stability tests."
	@echo "  ci-cd-stability-headless Run CI/CD stability tests in headless mode."
	@echo "  performance          Run performance tests in staging."
	@echo "  performance-production Run performance tests in production."
	@echo "  regression           Run full regression suite."
	@echo "  feature              Run feature-specific tests."
	@echo "  debug-explore        Debug explore page tests with verbose output."
	@echo "  debug-explore-headless Debug explore page tests in headless mode."
	@echo "  run-tests            Run a specific test or test pattern. Specify TEST, ENV, etc."

