import click
import subprocess
from mlflow.tracking import MlflowClient
import mlflow
import os
from pathlib import Path

# Set MLflow tracking URI
mlflow.set_tracking_uri(uri="http://localhost:5000")

@click.command()
@click.option('--model_name', required=True, help='Name of the model as it appears in the MLFlow registry.')
@click.option('--model_version', required=True, help='Version of the model as it appears in the MLFlow registry.')
@click.option('--status', required=True, type=click.Choice(['Staging', 'Production', 'Archived']),
    help='Status to which the model is promoted.')
@click.option('--test_set', required=True, help='Test dataset required for promotion to Production.')
def promote(model_name, model_version, status, test_set):
    """Promote a model in MLFlow after running tests if necessary.""" 
    client = MlflowClient()
    # Get current model version details
    model_version_details = client.get_model_version(name=model_name, version=model_version)
    current_stage = model_version_details.current_stage
    print(f"Current stage: {current_stage}")
    # Promotion from None to Staging
    if current_stage == "None" and status == "Staging":
        client.transition_model_version_stage(
            name=model_name,
            version=model_version,
            stage=status
        )
        print(f"Model {model_name} version {model_version} has been promoted from None to {status}")
    
    # Promotion from Staging to Production
    elif current_stage == "Staging" and status == "Production":
        os.environ["TEST_MODEL_NAME"] = model_name
        os.environ["TEST_MODEL_VERSION"] = model_version
        os.environ["TEST_TEST_SET"] = test_set
        current_file = Path(__file__).resolve()
        tests_path = current_file.parent / 'tests'
        test_result = subprocess.run(
            ["pytest", str(tests_path)],
            capture_output=True,
            text=True
        )
        # Promote if tests pass
        if test_result.returncode == 0:
            client.transition_model_version_stage(
                name=model_name,
                version=model_version,
                stage=status
            )
            print(f"Model {model_name} version {model_version} has been promoted from Staging to {status}")
        else:
            print(f"No change in status. Current stage: {current_stage}, Because the tests didn't pass")
    # Promotion from Production to Archived
    elif current_stage == "Production" and status == "Archived" :
        client.transition_model_version_stage(
        name=model_name,
        version=model_version,
        stage=status
    )
        print(f"Model {model_name} version {model_version} has been promoted from Proction to {status}")
    else:
        print(f"No change in status. Current stage: {current_stage}, status: {status}")

    


if __name__ == '__main__':
    promote()
