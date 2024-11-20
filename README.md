# MLOPS

# MLflow Usage Instructions

- To use MLflow, remember to start the server in the `mlflow` directory with the command:

```mlflow server```

- To run tests, type at the root:
  ```pytest```

-To install the package, use:
``` pip install -e .```


- Example of Using the Module
```predict --model_name LR-production --model_version 1 --input_file "data/archive/train.csv" --output_file "prediction.csv"```

setup.py 
entry_points={
        'console_scripts': [
            'predict=sentiment_analyser.predict:main' 
        ],# la commande # le package # le fichier # la fpnction

```promote --model_name LR-staging --model_version 1 --status Production --test_set data/archive/test.csv```
```promote --model_name LR-staging --model_version 1 --status Staging --test_set /data/archive/test.csv   ```
```promote --model_name LR-production --model_version 1 --status Archived --test_set data/archive/test.csv```
```retrain --model_name LR-production --model_version 1 --training-set data/archive/train.csv --training-set-id dataset_003 --register-updated-model```