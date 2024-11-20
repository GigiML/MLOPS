import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient
class ModelManager:
    def __init__(self, model_name, model_version, mlflow_url):
        self.model_name = model_name
        self.model_version = model_version
        self.mlflow_url = mlflow_url
        mlflow.set_tracking_uri(self.mlflow_url)
        self.model = self.load_model()
        self.client = MlflowClient()

    def load_model(self):
        """Load the model from MLFlow."""
        mlflow.set_tracking_uri(self.mlflow_url)
        return mlflow.sklearn.load_model(f"models:/{self.model_name}/{self.model_version}")

    def predict(self, input_data):
        """Predict the polarity of input data."""
        return self.model.predict(input_data)

    def predict_from_file(self, file_path):
        """Read messages from a CSV file and predict their polarity."""
        df = pd.read_csv(file_path)
        if 'review' not in df.columns:
            raise ValueError("CSV must contain a 'review' column.")
        predictions = self.predict(df['review'])
        return predictions
    
    def retrain(self, training_set, training_set_id=None, register_updated_model=False):
        """Retrain the model using new data without changing its training configuration."""
        
        df_train = pd.read_csv(training_set)
        X_train = df_train['review']
        y_train = df_train['polarity']
        
        with mlflow.start_run() as run:
            self.model.fit(X_train, y_train)
            
            tags = {
                "retrained": "True",
                "parent_version": self.model_version
            }
            if training_set_id:
                tags["training_set_id"] = training_set_id
            
            mlflow.set_tags(tags)
            
            mlflow.sklearn.log_model(self.model, "model")
            
            if register_updated_model:
                new_model_version = mlflow.register_model(f"runs:/{run.info.run_id}/model", self.model_name)
                self.client.set_model_version_tag(self.model_name, new_model_version.version, "retrained", "True")
                self.client.set_model_version_tag(self.model_name, new_model_version.version, "parent_version", self.model_version)
                if training_set_id:
                    self.client.set_model_version_tag(self.model_name, new_model_version.version, "training_set_id", training_set_id)
                
                print(f"Model {self.model_name} version {new_model_version.version} has been registered.")
            else:
                print(f"Model has been retrained. Run ID: {run.info.run_id}")

