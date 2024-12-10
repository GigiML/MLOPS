import click
import mlflow
import mlflow.sklearn

# export SENTIMENT_ANALYZER_MODEL_PATH=/tmp/sentiment-analyzer-model
@click.command()
@click.option("--mlflow_server_uri", default='http://127.0.0.1:5000', type=str, help='MLFlow server URL.')
@click.option("--model_name",default="LR-staging")
@click.option("--model_version",default="1")
@click.option("--target_path",default="/tmp/sentiment-analyzer-model")

def main(mlflow_server_uri, model_name, model_version, target_path):
    mlflow.set_tracking_uri(mlflow_server_uri)
    model = mlflow.sklearn.load_model(model_uri=f'models:/{model_name}/{model_version}')
    mlflow.sklearn.save_model(model,target_path)

if __name__ == "__main__":
    main()