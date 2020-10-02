###
# NeoTest Automation Framework Makefile
##

PKG := dist/$(shell python setup.py --fullname).tar.gz

.PHONY: clean install
.PHONY: travis
.PHONY: test testslide
.PHONY: venv venv-shell
.PHONY: pypi-package pypi-upload testpypi-upload
.PHONY: $(PKG)

test: testslide

testslide: venv
	. venv/bin/activate; \
		python -m pip install -qqq -U testslide; \
		testslide tests/*/testslide_*.py

testpypi-upload: pypi-package
	python -m twine upload --repository testpypi dist/*

pypi-upload: pypi-package
	python -m twine upload --repository pypi dist/*

pypi-package: $(PKG)

$(PKG):
	python setup.py sdist bdist_wheel

venv-shell: venv
	. venv/bin/activate; \
		$(SHELL); 

venv: venv/bin/activate

venv/bin/activate: requirements.txt $(PKG)
	test -d venv || virtualenv venv
	. venv/bin/activate; \
		python -m pip install -qqq --upgrade pip; \
		python -m pip install -qqq -Ur requirements.txt; \
		python -m pip install --force-reinstall $(PKG); \
	touch venv/bin/activate

travis: $(PKG)
	python -m pip install -qqq --upgrade pip;
	python -m pip install -qqq -Ur requirements.txt;
	python -m pip install $(PKG);
	neotest --help

clean:
	python -m pip uninstall neotest
	python setup.py clean --all
	rm -rf dist *.egg-info
	rm -rf venv
	find -iname "*.pyc" -delete
