import click
from sentiment_analyzer.model_manager import ModelManager

@click.command()
@click.option('--model_name', required=True, help='Name of the model as it appears in the MLFlow registry.')
@click.option('--model_version', required=True, help='Version of the model as it appears in the MLFlow registry.')
@click.option('--mlflow_url', default='http://localhost:5000', type=str, help='MLFlow server URL.')
@click.option('--training-set', required=True, help='New training dataset to use for retraining.')
@click.option('--training-set-id', help='Optional identifier for the training dataset.')
@click.option('--register-updated-model', is_flag=True, help='If set, automatically register the model in MLFlow registry as a new version.')
def retrain(model_name, model_version, mlflow_url, training_set, training_set_id, register_updated_model):
    """Retrain a model using new data without changing its training configuration."""
    model_manager = ModelManager(model_name=model_name, model_version=model_version, mlflow_url=mlflow_url)
    model_manager.retrain(training_set, training_set_id, register_updated_model)

if __name__ == '__main__':
    retrain()