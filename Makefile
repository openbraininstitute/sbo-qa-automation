setup:
	uv install --upgrade
	uv lint
	@echo "Environment setup complete. Use 'uv' commands to run tests and linting."


production:
	# uv run pytest tests/test_login.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_build.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	uv run pytest tests/test_explore_page.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_explore_ndensity.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv

staging:
	uv run pytest tests/test_login.py --env=staging --env_url=staging --browser-name=firefox $(HEADLESS) -sv

sauce-labs:
	uv run pytest tests/test_login.py --env=sauce-labs --env_url=sauce-lab --browser-name=firefox $(HEADLESS) -sv