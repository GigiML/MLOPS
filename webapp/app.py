from fastapi import FastAPI
from pydantic import BaseModel
import os
import numpy as np
import pickle
import uvicorn
import pandas as pd

app = FastAPI(
    title="Sentiment Analysis API",
    version="1.0.0",
    description="An API for predicting sentiment of reviews using a pre-trained model."
)

model = pickle.load(open(os.getenv("SENTIMENT_ANALYZER_MODEL_PATH",default="/model")+"/model.pkl", 'rb'))

class PredictInput(BaseModel):
    reviews: list[str]
    model_config = {
        "json_schema_extra": {
            "example": {
                "reviews": ["c'est un bon film", "c'est un mauvais film"]
            }
        }
    }

@app.post("/predict", summary="Predict sentiment of reviews")
def predict(input: PredictInput):
    """
    Predicts the sentiment of given reviews.
    
    Args:
        input (PredictInput): A list of reviews to analyze.
        
    
    Returns:
        dict: A dictionary containing a list of sentiments ("positif" or "négatif") for each review.
        
        
    Example:
        Request body:
        {
            "reviews": ["c'est un bon film", "c'est un mauvais film"]
        }
        
        Response:
        {
            "sentiments": ["positif", "négatif"]
        }
    """
    pred = model.predict(input.reviews)
    sentiments = ["positif" if p == 1 else "négatif" for p in pred]
    return {"sentiments": sentiments}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
#uvicorn app:app --host 0.0.0.0