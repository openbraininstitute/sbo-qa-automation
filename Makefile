setup:
	uv install --upgrade
	uv lint
	@echo "Environment setup complete. Use 'uv' commands to run tests and linting."


production: | venv
	uv run pytest tests/test_login.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv

staging: | venv
	uv run pytest tests/test_login.py --env=staging --env_url=staging --browser-name=firefox $(HEADLESS) -sv

sauce-labs: | venv
	uv run pytest tests/test_login.py --env=sauce-labs --env_url=sauce-lab --browser-name=firefox $(HEADLESS) -sv