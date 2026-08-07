.PHONY: clean clean-build clean-pyc clean-test check coverage dist docs format format/ruff help install lint lint/flake8 lint/black lint/ruff lint/ruff-format lint/mypy test test-all
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint/flake8: ## check style with flake8 (legacy)
	flake8 src/healthy_api tests
lint/black: ## check style with black (legacy)
	black --check src/healthy_api tests
lint/ruff: ## lint with ruff
	python -m ruff check src/healthy_api tests
lint/ruff-format: ## check formatting with ruff
	python -m ruff format --check src/healthy_api tests
lint/mypy: ## type-check with mypy
	python -m mypy src/healthy_api

format: ## format with ruff (via script/format)
	./script/format
format/ruff: format ## alias for format

lint: lint/ruff-format lint/ruff lint/mypy ## check format, lint, and types (CI gates)

test: ## run tests quickly with the default Python
	python -m pytest

check: lint test ## run lint and tests

test-all: ## run tests on every Python version with tox
	python -m tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source src/healthy_api -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/healthy_api.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src/healthy_api
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload --verbose dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
