SRCPATH := $(shell pwd)
PROJECTNAME := $(shell basename $(CURDIR))
ENTRYPOINT := $(PROJECTNAME).ini
VIRTUAL_ENVIRONMENT := $(CURDIR)/.venv
LOCAL_PYTHON := $(VIRTUAL_ENVIRONMENT)/bin/python3

define HELP
Manage $(PROJECTNAME). Usage:

make run        - Run $(PROJECTNAME).
make restart    - Restart systemd service.
make install    - Build application for the first time.
make update     - Update pip deploy in both poetry and pipenv environments.
make format     - Format source code and sort imports.
make clean      - Remove cached files and lock files.
make lint       - Check code formatting with flake8

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
	service $(PROJECTNAME) start


.PHONY: restart
restart: env
	service $(PROJECTNAME) stop
	make clean
	service $(PROJECTNAME) start
	service $(PROJECTNAME) status


.PHONY: install
install:
	make clean
	if [ ! -d "./.venv" ]; then python3 -m venv $(VIRTUAL_ENVIRONMENT); fi
	. $(VIRTUAL_ENVIRONMENT)/bin/activate
	$(LOCAL_PYTHON) -m pip install --upgrade pip setuptools wheel
	$(LOCAL_PYTHON) -m pip install -r requirements.txt


.PHONY: update
update: env
	$(LOCAL_PYTHON) -m pip install -U pip
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