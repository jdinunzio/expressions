.PHONY: help lint flake docstyle typecheck black-check black-fix
.PHONY: test-unit test-integration tests coverage
.PHONY: report-test-unit report-test-integration report-test report-lint project-init

# General Configuration
SHELL               := /bin/bash

help:                      ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


##
##Run Services
##

run-be-dev:                # # Run backend in foreground, in development mode
	@UVICORN_EXTRA_PARAMS="--reload" poetry run src/expressions/presentation/be_service.sh

run-be:                    # # Run backend in foreground
	poetry run src/expressions/presentation/be_service.sh


##
##Development
##

lint:                      ## Code Linting
	@poetry run pylint --version
	@poetry run pylint src tests

flake:                     ## Flake-8 and ruff
	@poetry run ruff --version
	@poetry run ruff src tests
	@poetry run flake8 --version
	@poetry run flake8 --config=.flake8 src tests

docstyle:                  ## Check Style of docstrings
	@poetry run pydocstyle --version
	@poetry run pydocstyle src/ tests/

typecheck:                 ## Typecheck
	@poetry run mypy --version
	@poetry run mypy src tests

black-check:               ## Code checking with black
	@poetry run black --version
	@poetry run black --check --diff src tests

black-fix:                 ## Code formatting with black
	@poetry run isort src tests
	@poetry run black src tests

dev-check:                 ## Run common development checks
	@echo '**** Linting....'
	@make --no-print-directory lint
	@echo -e '\n\n**** Flaking...'
	@make --no-print-directory flake
	@echo -e '\n\n**** Blacking...'
	@make --no-print-directory black-check
	@echo -e '\n\n**** Docstyling...'
	@make --no-print-directory docstyle
	@echo -e '\n\n**** Type checking...'
	@make --no-print-directory typecheck
	@echo -e '\n\n**** Unit Testing...'
	@make --no-print-directory test-unit
	@echo -e '\n\n'

##
##Testing
##

test-unit:                 ## Run unit tests
	@poetry run green -vvvq tests/unit

test-integration:          ## Run integration tests
	@poetry run green -vvvq tests/integration

tests:                     ## Run all tests
	@make test-unit
	@make test-integration

coverage:                  ## Code coverage
	@poetry run green -vvvq --run-coverage test/unit

report-test-unit:          ## Generate junit report for unit tests
	@poetry run python -m xmlrunner discover -o ./reports/junit/tests/unit tests/unit/

report-test-integration:   ## Generate junit report for integration tests
	@poetry run python -m xmlrunner discover -o ./reports/junit/tests/integration tests/integration/

report-test:               ## Generate junit report for tests
	@make report-test-unit
	@make report-test-integration

report-lint:               ## Generate text and junit report for linting
	@poetry run flake8 . --output-file=reports/flake8.txt
	@poetry run flake8_junit reports/flake8.txt reports/junit/lint/flake8_junit.xml

# #
# #Docker
# #

#docker-build:              # # Build docker image
#	@docker build -t expressions:latest .

#docker-run-be-dev:         # # Run backend in foreground using docker, in development mode
#	@UVICORN_EXTRA_PARAMS="--reload" docker run --rm -it -p 3380:3380 expressions:latest run-be-dev

##
##CI Related and Bootstrapping
##

project-init:              ## Initializes virtual environment for this project
	@python -m venv .venv
	@source .venv/bin/activate && pip install -U pip && pip install poetry==1.4 && poetry install
