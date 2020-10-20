SRCPATH := $(shell pwd)
PROJECTNAME := $(shell basename $(CURDIR))
ENTRYPOINT := $(PROJECTNAME).ini

define HELP
Manage $(PROJECTNAME). Usage:

make run        - Run $(PROJECTNAME).
make restart    - Purge cache & reinstall modules.
make deploy     - Pull latest build and deploy to production.
make update     - Update pip deploy in both poetry and pipenv environments.
make clean      - Remove cached files and lock files.
endef
export HELP


.PHONY: run restart deploy update clean help


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


.PHONY: deploy
deploy:
	service $(PROJECTNAME) stop
	git stash
	git pull origin master
	$(shell . ./deploy.sh)
	service $(PROJECTNAME) start
	service $(PROJECTNAME) status


.PHONY: update
update: env
	.venv/bin/python3 -m pip install -U pip
	poetry update
	poetry export -f requirements.txt --output requirements.txt --without-hashes


.PHONY: format
format: env
	$(shell . .venv/bin/activate && isort -rc ./)
	$(shell . .venv/bin/activate && black ./)


.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name 'poetry.lock' -delete
	find . -name 'Pipefile.lock' -delete