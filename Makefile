###
# NeoTest Automation Framework Makefile
##

PKG := dist/$(shell python setup.py --fullname).tar.gz

BLACK    := black --line-length=120 --diff --check neotest
BLACKIFY := black --line-length=120 neotest
ISORT    := isort --check-only --profile black --diff neotest
ISORTIFY := isort --profile black neotest
FLAKE    := flake8 --count --max-line-length=120 --show-source --statistics neotest


VENV := . venv/bin/activate && # with one whitespace

.PHONY: clean install
.PHONY: travis travis-install
.PHONY: black blackify isort isortify flake
.PHONY: test testslide
.PHONY: venv vsh
.PHONY: pypi-package pypi-upload testpypi-upload
.PHONY: $(PKG)

test: testslide black isort flake

testslide: venv
	$(VENV)testslide tests/*/testslide_*.py

testpypi-upload: pypi-package
	python -m twine upload --repository testpypi dist/*

pypi-upload: pypi-package
	python -m twine upload --repository pypi dist/*

pypi-package: $(PKG)

$(PKG):
	python setup.py sdist bdist_wheel

vsh: venv
	$(VENV)$(SHELL)

venv: venv/bin/activate

venv/bin/activate: requirements.txt requirements-dev.txt $(PKG)
	test -d venv || virtualenv venv
	$(VENV)python -m pip install -q --upgrade pip
	$(VENV)pip install -q -Ur requirements.txt
	$(VENV)pip install -q -Ur requirements-dev.txt
	$(VENV)pip install --force-reinstall $(PKG)
	touch venv/bin/activate

black: venv
	$(VENV)$(BLACK)

blackify: venv
	$(VENV)$(BLACKIFY)

isort: venv
	$(VENV)$(ISORT)

isortify: venv
	$(VENV)$(ISORTIFY)

flake: venv
	$(VENV)$(FLAKE)

travis: travis-install
	$(FLAKE)
	$(ISORT)
	$(BLACK)

travis-install: $(PKG)
	python -m pip install -q --upgrade pip
	pip install -q -r requirements.txt
	pip install -q -r requirements-dev.txt
	pip install $(PKG)
	neotest --help

clean:
	python -m pip uninstall neotest
	python setup.py clean --all
	rm -rf dist *.egg-info
	rm -rf venv
	find -iname "*.pyc" -delete
