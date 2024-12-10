#!/bin/bash


# API URL
export url_api=http://localhost:8000/predict

# Model path
export SENTIMENT_ANALYZER_MODEL_PATH=/tmp/sentiment-analyzer-model

# Test model information
export TEST_MODEL_NAME=LR-production
export TEST_MODEL_VERSION=1

# Test set path
export TEST_TEST_SET=data/archive/test.csv

# Optional: Print confirmation message
echo "Environment variables have been set."