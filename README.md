# MLOps Project 🚀

Welcome to the Sentiment Analyzer Tool! 🌟 This tool allows you to perform sentiment analysis on text data using pre-trained models. Below are the instructions on how to use the tool effectively.



## Table of Contents

- [MLOps Project 🚀](#mlops-project-)
  - [Table of Contents](#table-of-contents)
  - [Sentiment Analyzer Tool](#sentiment-analyzer-tool)
  - [🚀 Quick Start](#-quick-start)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
      - [1. Create a venv and Install the Dependencies](#1-create-a-venv-and-install-the-dependencies)
      - [2. Install the command tool](#2-install-the-command-tool)
    - [Running Tests](#running-tests)
    - [Making Predictions](#making-predictions)
    - [Promoting Models](#promoting-models)
    - [Retraining Models](#retraining-models)
    - [Getting Started](#getting-started)
      - [Prerequisites](#prerequisites-1)
      - [Installation Steps](#installation-steps-1)
  - [Sentiment Analyzer Web Application](#sentiment-analyzer-web-application)
    - [Getting Started](#getting-started-1)
    - [Running the Web Application](#running-the-web-application)
    - [Making Predictions](#making-predictions-1)
    - [Using the Frontend Application](#using-the-frontend-application)
    - [Docker Deployment](#docker-deployment)
    - [Using the Makefile](#using-the-makefile)
  - [MLflow Usage Instructions](#mlflow-usage-instructions)
    - [Model Management Commands](#model-management-commands)
      - [Predict](#predict)
      - [Promote Model](#promote-model)
      - [Retrain Model](#retrain-model)
  - [Project Structure](#project-structure)

## Sentiment Analyzer Tool
## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker
- MLflow
- Virtual Environment Support

### Installation Steps

#### 1. Create a venv and Install the Dependencies

```sh
make venv
```

#### 2. Install the command tool

```sh
make install
```


### Running Tests

To ensure the model's reliability, you can run a set of tests using the `make test` framework. These tests will verify the model's performance and accuracy. The model names and versions are configured in the `exports-var.sh` file.

### Making Predictions

You can use the `predict` command to calculate the sentiment polarity of one or more messages using pre-trained models.

```bash
predict --input_file <input_file> --output_file <output_file> --model_name <model_name> --model_version <model_version> --mlflow_url <mlflow_url>
```

```bash
predict --text <text> --model_name <model_name> --model_version <model_version> --mlflow_url <mlflow_url>
```

- `--input_file`: The input file containing the messages to be processed.
- `--output_file`: The output file to save the results.
- `--text`: A single text message to analyze.
- `--model_name`: The name of the model as registered in the MLFlow registry.
- `--model_version`: The version of the model as registered in the MLFlow registry.
- `--mlflow_url`: The URL of the MLFlow server (default is `http://localhost:5000`).

**Note:** Exactly one of the arguments `--text` and `--input_file` must be provided.

### Promoting Models

You can promote a model to different stages (Staging, Production, or Archived) using the `promote` command.

```bash
promote --model_name <model_name> --model_version <model_version> --status <status> --test-set <test_set>
```

- `--model_name`: The name of the model as registered in the MLFlow registry.
- `--model_version`: The version of the model as registered in the MLFlow registry.
- `--status`: The status to which the model is promoted (Staging, Production, or Archived).
- `--test-set`: The test dataset, required for promotion to Production.

**Note:** A model can only be promoted to the next status level and must pass the defined tests to be promoted to Production.

### Retraining Models

You can retrain a model using new data without changing its training configuration using the `retrain` command.

```bash
retrain --model_name <model_name> --model_version <model_version> --training-set <training_set> --training-set-id <training_set_id> --register-updated-model
```

- `--model_name`: The name of the model as registered in the MLFlow registry.
- `--model_version`: The version of the model as registered in the MLFlow registry.
- `--training-set`: The new training dataset to use.
- `--training-set-id`: Optional identifier for the training dataset.
- `--register-updated-model`: If set, automatically registers the updated model in the MLFlow registry as a new version.

**Note:** The following tags will be set:
- `retrained`: Set to True.
- `parent_version`: The version from which the model is rebuilt.
- `training_set_id`: If provided, will be associated with the model and the run.

### Getting Started

#### Prerequisites

- Python 3.11+
- Docker
- MLflow
- Virtual Environment Support

#### Installation Steps

1. **Create a venv and Install the Dependencies**

    ```bash
    make venv
    ```

2. **Install the command tool**

    ```bash
    make install
    ```

## Sentiment Analyzer Web Application

### Getting Started

1. **Install Docker**: Ensure Docker is installed on your system. You can download Docker Desktop from the official website.

2. **Clone the Repository**: Clone the repository containing the Sentiment Analyzer Web Application.

3. **Set Environment Variables**: Source the `exports-var.sh` file to set the necessary environment variables.

    ```sh
    source exports-var.sh
    ```

### Running the Web Application

**Build the Docker Image**: Navigate to the `webapp` directory and build the Docker image using the Makefile.

```bash
make build-webapp
```

**Run the Docker Container**: Run the Docker container to start the web application.

```bash
make run-docker-webapp
```

### Making Predictions

**Access the Documentation**: The web application provides automatic documentation accessible at `http://localhost:8001/docs`.

**Use the `/predict` Endpoint**: The `/predict` endpoint allows you to make predictions on text data.
- **Input**: A JSON structure like `{"reviews":["c'est un bon film","c'est un mauvais film"]}`.
- **Output**: A JSON structure like `{"sentiments":["positif","negatif"]}`.

**Test the Endpoint**: Use the "Try it out" button in the documentation to test the `/predict` endpoint with sample data.

### Using the Frontend Application

**Build the Frontend Docker Image**:

```bash
make build-docker-front
```

### Docker Deployment

**Build the Docker Compose Services**:

```bash
make built-run-docker-compose
```

**Access the Application**:
- Frontend: `http://localhost:8501`

### Using the Makefile

- **Start MLflow Server**

    ```bash
    make server
    ```

- **Run Tests**

    ```bash
    make test
    ```

- **Build Webapp**

    ```bash
    make build-webapp
    ```

- **Run Docker Containers**

    ```bash
    make run-docker-webapp
    make run-docker-front
    ```

## MLflow Usage Instructions

- **Start MLflow Server**

    ```bash
    make server
    ```

- **Run Tests**

    ```bash
    make test
    ```

- **Build Webapp**

    ```bash
    make build-webapp
    ```

- **Run Docker Containers**

    ```bash
    make run-docker-webapp
    make run-docker-front
    ```

### Model Management Commands

#### Predict

```bash
predict --model_name LR-production \
        --model_version 1 \
        --input_file "data/train.csv" \
        --output_file "prediction.csv"
```

#### Promote Model

```bash
promote --model_name LR-staging \
        --model_version 1 \
        --status Production \
        --test_set data/test.csv
```

#### Retrain Model

```bash
retrain --model_name LR-production \
        --model_version 1 \
        --training-set data/train.csv \
        --training-set-id dataset_003 \
        --register-updated-model
```

## Project Structure

```text
mlops-project/
│
├── mlflow/                 # MLflow tracking server
├── src/                    # Source code
│   ├── webapp/             # Web application
│   ├── tests/              # Test suite
│   ├── sentiment-analyzer/ # Python package
│   └── frontend/           # Frontend components
├── data/                   # Dataset storage
├── Makefile                # Build and development commands
├── setup.py                # Configuration file for Python package
├── exports-var.sh          # Environment variable file
└── requirements.txt        # Project dependencies
```

- To use MLflow, remember to start the server in the `mlflow` directory with the command:

    ```bash
    mlflow server
    ```

- To run tests, type at the root:

    ```bash
    pytest
    ```

- To install the package, use:

    ```bash
    pip install -e .
    ```

- Example of Using the Module

    ```bash
    predict --model_name LR-production --model_version 1 --input_file "data/archive/train.csv" --output_file "prediction.csv"
    ```



- Example Commands

    ```bash
    promote --model_name LR-staging --model_version 1 --status Production --test_set data/archive/test.csv
    ```

    ```bash
    promote --model_name LR-staging --model_version 1 --status Staging --test_set /data/archive/test.csv
    ```

    ```bash
    promote --model_name LR-production --model_version 1 --status Archived --test_set data/archive/test.csv
    ```

    ```bash
    retrain --model_name LR-production --model_version 1 --training-set data/archive/train.csv --training-set-id dataset_003 --register-updated-model
    ```