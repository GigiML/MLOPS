import click
import subprocess
from sentiment_analyser.model_manager import ModelManager
import mlflow

@click.command()
@click.option('--model_name', required=True, help='Name of the model as it appears in the MLFlow registry.')
@click.option('--model_version', required=True, help='Version of the model as it appears in the MLFlow registry.')
@click.option('--status', required=True, type=click.Choice(['Staging', 'Production', 'Archived']),
    help='Status to which the model is promoted.')
@click.option('--test_set', required=True, help='Test dataset required for promotion to Production.')
def promote(model_name, model_version, status, test_set):
    """Promote a model in MLFlow after running tests if necessary.""" 
    valid_statuses = ['Staging', 'Production', 'Archived']
    

if __name__ == '__main__':
    promote()
