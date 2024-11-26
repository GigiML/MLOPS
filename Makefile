VENV_NAME := venv
PYTHON := python3.11
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

docker:
	$(VENV_ACTIVATE) && colima start

run-api:
	$(VENV_ACTIVATE) && rm -rf /tmp/sentiment-analyzer-model/ && $(PYTHON) webapp/get_mlflow_model.py && uvicorn webapp.app:app --host 0.0.0.0

build:
	cd webapp && docker build -t sentiment-analyzer:1-LR-staging-1 \
    --build-arg MLFLOW_SERVER_URI=http://host.docker.internal:5000 \
    --build-arg MODEL_NAME=LR-staging \
    --build-arg MODEL_VERSION=1 \
    .


run-docker:
	cd webapp && 
	docker run -p 8001:8000 --name sentiment-analyzer-container sentiment-analyzer:1-LR-staging-1