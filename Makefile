VENV_NAME := venv
PYTHON := python3.12
VENV_ACTIVATE := . $(VENV_NAME)/bin/activate

.PHONY: venv install server test clean

venv:
	$(PYTHON) -m venv $(VENV_NAME)
	$(VENV_ACTIVATE) && pip install -r requirements.txt

install:
	$(VENV_ACTIVATE) && pip install -e .

server:
	$(VENV_ACTIVATE) && cd mlflow && mlflow server

test:
	$(VENV_ACTIVATE) && pytest

clean:
	rm -rf $(VENV_NAME)