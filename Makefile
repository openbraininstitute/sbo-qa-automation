setup:
	uv install --upgrade
	uv lint
	@echo "Environment setup complete. Use 'uv' commands to run tests and linting."


production:
	# uv run pytest tests/test_login.py tests/test_explore_page.py tests/test_morphology.py tests/test_explore_ephys.py tests/test_explore_ndensity.py tests/test_explore_model.py tests/test_build.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	# uv run pytest tests/test_login.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	# uv run pytest tests/test_landing.py tests/test_login.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	uv run pytest tests/test_build.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	# uv run pytest tests/test_explore_page.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_morphology.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_explore_ndensity.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_sandbox.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_homepage.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_vl_overview.py --env=production --env_url=production --browser-name=firefox $(HEADLESS) -sv


staging:
	uv run pytest tests/test_login.py --env=staging --env_url=staging --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_landing.py --env=staging --env_url=staging --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_login.py tests/test_morphology.py tests/test_explore_ephys.py tests/test_explore_ndensity.py tests/test_explore_model.py tests/test_build.py --env=staging --env_url=staging --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_login.py tests/test_morphology.py  --env=staging --env_url=staging --browser-name=firefox $(HEADLESS) -sv
	#uv run pytest tests/test_landing.py tests/test_login.py tests/test_morphology.py tests/test_explore_ephys.py tests/test_explore_ndensity.py tests/test_explore_model.py tests/test_build.py --env=staging --env_url=staging --browser-name=firefox $(HEADLESS) -sv

