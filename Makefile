SRCPATH := $(shell pwd)
PROJECT_NAME := $(shell basename $(CURDIR))
VIRTUAL_ENVIRONMENT := $(PROJECT_NAME)/.venv
LOCAL_PYTHON := .venv/bin/python3

define HELP
Manage $(PROJECT_NAME). Usage:

make run        - Run $(PROJECT_NAME).
make restart    - Restart systemd service (if exists).
make install    - Build environment & install dependencies.
make update     - Update depenencies with Poetry & outout new requirements.txt.
make format     - Format source code and sort imports.
make clean      - Remove cached files, lockfiles, and other unnessecary junk.
make lint       - Check code formatting with flake8.

endef
export HELP


.PHONY: run restart install update format clean lint help


requirements: .requirements.txt
env: .venv/bin/activate


.requirements.txt: requirements.txt
	$(shell . .venv/bin/activate && pip install -r requirements.txt)


.venv/bin/activate:
	python3 -m venv .venv


all help:
	@echo "$$HELP"


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
	. .venv/bin/activate
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


.PHONY: lint
lint:
	flake8 . --count \
			--select=E9,F63,F7,F82 \
			--exclude .git,.github,__pycache__,.pytest_cache,.venv,logs,creds,.venv,docs,logs \
			--show-source \
			--statistics


.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name 'poetry.lock' -delete
	find . -name '*.log' -delete
	find . -wholename './logs/*.log' -delete
	find . -wholename 'logs/*.json' -delete
	find . -wholename '.pytest_cache' -delete
	find . -wholename '*/.pytest_cache' -delete
