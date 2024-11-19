import mlflow
import pandas as pd

class ModelManager:
    def __init__(self, model_name, model_version, mlflow_url):
        self.model_name = model_name
        self.model_version = model_version
        self.mlflow_url = mlflow_url
        self.model = self.load_model()

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
    
    