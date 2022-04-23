PROJECT_NAME := $(shell basename $CURDIR)
VIRTUAL_ENVIRONMENT := $(CURDIR)/.venv
LOCAL_PYTHON := $(VIRTUAL_ENVIRONMENT)/bin/python3

define HELP
Manage $(PROJECT_NAME). Usage:

make run        - Run project locally.
make restart    - Restart systemd service (if exists).
make install    - Create Python virtual environment & install dependencies.
make update     - Update depenencies to latest version & output new `requirements.txt`.
make format     - Format source code and sort imports.
make test       - Run test suite.
make lint       - Check code formatting with flake8.
make clean      - Remove cached files, lockfiles, and other unnecessary junk.

endef
export HELP


.PHONY: run restart install update format test lint clean help


all help:
	@echo "$$HELP"

env: .venv/bin/activate

.PHONY: run
run: env
	uwsgi --ini broiestbot.ini


.PHONY: restart
restart: env
	service $(PROJECT_NAME) stop
	make clean
	service $(PROJECT_NAME) start
	service $(PROJECT_NAME) status


.PHONY: install
install:
	if [ ! -d "./.venv" ]; then python3 -m venv $(VIRTUAL_ENVIRONMENT); fi
	$(shell . .venv/bin/activate)
	$(LOCAL_PYTHON) -m pip install --upgrade pip setuptools wheel
	$(LOCAL_PYTHON) -m pip install -r requirements.txt


.PHONY: update
update: env
	$(LOCAL_PYTHON) -m pip install -U pip setuptools wheel
	poetry update
	poetry export -f requirements.txt --output requirements.txt --without-hashes


.PHONY: format
format: env
	isort --multi-line=3 .
	black .


.PHONY: test
test: env
	pytest


.PHONY: lint
lint:
	flake8 . --count \
			--select=E9,F63,F7,F82 \
			--exclude .git,.github,__pycache__,.pytest_cache,.venv,logs,creds,.venv,docs,logs \
			--show-source \
			--statistics


.PHONY: clean
clean:
	find . -name '**/*.pyc' -delete
	find . -name 'poetry.lock' -delete
	find . -name '**/*.log' -delete
	find . -wholename './logs/*.log' -delete
	find . -wholename 'logs/*.json' -delete
	find . -wholename '**/__pycache__' -delete
	find . -wholename '**/.pytest_cache' -delete
