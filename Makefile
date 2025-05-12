.PHONY: init activate update lint test run-tick

init:
	./bootstrap.sh

activate:
	@echo "Run: source venv/bin/activate"

update:
	pip install --upgrade -r requirements.txt

lint:
	flake8 scripts/ fats/

test:
	pytest -q

run-tick:
	python scripts/tick_collector.py
