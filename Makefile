.DEFAULT_GOAL := help
PYTHON := .venv/bin/python

.PHONY: help setup notebook check smoke
help:
	@printf '%s\n' 'make setup    Create Python 3.11 environment and install dependencies (requires uv)' 'make notebook Launch JupyterLab' 'make check    Validate primary notebooks and local links (no execution)' 'make smoke    Execute four offline solutions into artifacts/smoke'

setup:
	uv venv --python 3.11 --allow-existing .venv
	uv pip install --python $(PYTHON) -r requirements.txt

notebook:
	$(PYTHON) -m jupyterlab

check:
	$(PYTHON) -m unittest discover -s scripts -v
	$(PYTHON) scripts/check_notebooks.py

smoke:
	$(PYTHON) scripts/smoke_notebooks.py
