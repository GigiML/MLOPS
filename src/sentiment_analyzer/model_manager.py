import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient
class ModelManager:
    """
    A class to manage MLflow models, including loading, prediction, and retraining.

    Attributes:
        model_name (str): The name of the MLflow model.
        model_version (str): The version of the MLflow model.
        mlflow_url (str): The URL of the MLflow tracking server.
        model: The loaded MLflow model.
        client (MlflowClient): An instance of MlflowClient for interacting with MLflow.
    """
    def __init__(self, model_name, model_version, mlflow_url):
        """
        Initialize the ModelManager.

        Args:
            model_name (str): The name of the MLflow model.
            model_version (str): The version of the MLflow model.
            mlflow_url (str): The URL of the MLflow tracking server.
        """
        self.model_name = model_name
        self.model_version = model_version
        self.mlflow_url = mlflow_url
        mlflow.set_tracking_uri(self.mlflow_url)
        self.model = self.load_model()
        self.client = MlflowClient()

    def load_model(self):
        """Load the model from MLFlow.
         Returns:
            The loaded MLflow model.
        """
        mlflow.set_tracking_uri(self.mlflow_url)
        return mlflow.sklearn.load_model(f"models:/{self.model_name}/{self.model_version}")

    def predict(self, input_data):
        """
        Predict the polarity of input data.

        Args:
            input_data: The input data for prediction.

        Returns:
            Predictions for the input data.
        """
        return self.model.predict(input_data)

    def predict_from_file(self, file_path):
        """Read messages from a CSV file and predict their polarity.
        Returns:
            Predictions for the messages in the CSV file."""
        df = pd.read_csv(file_path)
        if 'review' not in df.columns:
            raise ValueError("CSV must contain a 'review' column.")
        predictions = self.predict(df['review'])
        return predictions
    
    def retrain(self, training_set, training_set_id=None, register_updated_model=False):
        """
        Retrain the model using new data without changing its training configuration.

        Args:
            training_set (str): Path to the CSV file containing the new training data.
            training_set_id (str, optional): An identifier for the training set.
            register_updated_model (bool): Whether to register the retrained model in MLflow.

        Returns:
            None
        """
        # Load and prepare the training data
        df_train = pd.read_csv(training_set)
        X_train = df_train['review']
        y_train = df_train['polarity']
        
        # Start an MLflow run for logging
        with mlflow.start_run() as run:
            self.model.fit(X_train, y_train)
            # Retrain the model
            tags = {
                "retrained": "True",
                "parent_version": self.model_version
            }
            if training_set_id:
                tags["training_set_id"] = training_set_id
            # Set tags for the run
            mlflow.set_tags(tags)
            # Log the retrained model
            mlflow.sklearn.log_model(self.model, "model")
            
            if register_updated_model:
                # Register the new model version
                new_model_version = mlflow.register_model(f"runs:/{run.info.run_id}/model", self.model_name)
                # Set tags for the new model version
                self.client.set_model_version_tag(self.model_name, new_model_version.version, "retrained", "True")
                self.client.set_model_version_tag(self.model_name, new_model_version.version, "parent_version", self.model_version)
                if training_set_id:
                    self.client.set_model_version_tag(self.model_name, new_model_version.version, "training_set_id", training_set_id)
                
                print(f"Model {self.model_name} version {new_model_version.version} has been registered.")
            else:
                print(f"Model has been retrained. Run ID: {run.info.run_id}")

