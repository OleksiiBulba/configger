### Variables ###
NAME = configger
VERSION = $(shell cat version.txt)
OS = $(shell uname -s)

#################

.PHONY: all
all: clean python

venv/touchfile: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	@echo "To activate python virtual environment, please run the command '. venv/bin/activate'"
	touch venv/touchfile

venv: venv/touchfile

.PHONY: init
init: venv

.PHONY: clean
clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf ./GameStateMachine.egg-info/
	@echo "Cleaning up byte compiled python stuff"
	find . -maxdepth 1 -type d -name "__pycache__" -delete
	@echo "Cleaning venv"
	rm -rf venv
	find -iname "*.pyc" -delete
	@echo "Please run 'deactivate' to deactivate python virtual environment"

.PHONY: python
python:
	. venv/bin/activate; python setup.py build

.PHONY: install
install:
	. venv/bin/activate; python setup.py install

.PHONY: version
version:
	@echo $(VERSION)
