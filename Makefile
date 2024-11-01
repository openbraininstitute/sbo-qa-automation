venv:
	if python -m ensurepip --version; then python -m venv $@; else virtualenv $@; fi
	venv/bin/pip install --upgrade pip
	venv/bin/pip install pycodestyle pylint

setup-venv: venv
	@echo "Virtual environment created. Run 'source venv/bin/activate' to activate."

lint: | venv
	venv/bin/pycodestyle --config=.pycodestyle *.py
	venv/bin/pylint *.py