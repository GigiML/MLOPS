import mlflow.pyfunc
import pytest
import os
import numpy as np
import pandas as pd
# export TEST_MODEL_NAME=LR-production
# export TEST_MODEL_VERSION=1
# export TEST_TEST_SET=/data/archive/test.csv
mlflow.set_tracking_uri(uri="http://localhost:5000")

@pytest.fixture
def load_model():
    """Load the model from MLFlow registry."""
    model_name = os.getenv("TEST_MODEL_NAME")
    model_version = os.getenv("TEST_MODEL_VERSION")
    model = mlflow.sklearn.load_model(f"models:/{model_name}/{model_version}")
    return model

def test_usual_input(load_model):
    txt = "Si vous cherchez du cinéma abrutissant à tous les étages,n'ayant aucune peur du cliché en castagnettes et moralement douteux, est fait pour vous.Toutes les productions Besson,via sa filière EuropaCorp ont de quoi faire naître la moquerie.Paris y est encore une fois montrée comme une capitale exotique,mais attention si l'on se dirige vers la banlieue,on y trouve tout plein d'intégristes musulmans prêts à faire sauter le caisson d'une ambassadrice américaine.Nauséeux.Alors on se dit qu'on va au moins pouvoir apprécier la déconnade d'un classique buddy-movie avec le jeune agent aux dents longues obligé de faire équipe avec un vieux lou complètement timbré.Mais d'un côté,on a un Jonathan Rh"
    df = pd.DataFrame(data={"review": [txt]})
    output = load_model.predict(df)
    print(type(output[0]))
    assert isinstance(output, np.ndarray)
    assert isinstance(output[0], np.int64)


def test_unusual_input(load_model):
    df = pd.DataFrame(data={"review": ["", "$*%1&"]})
    output = load_model.predict(df)
    print(output)
    assert isinstance(output, np.ndarray)
    assert isinstance(output[0], np.int64)

def test_obvious_output(load_model):
    test_cases = pd.DataFrame({
        "review": ["Ce film est génial", "Très bon film", "film trés mauvais ne recommande pas, Nauséeux, ennuyeux"],
        "expected_output": [1, 1, 0]
    })
    output = load_model.predict(test_cases["review"])
    for expected, result in zip(test_cases["expected_output"], output):
        assert result == expected , f"Expected {expected}, but got {result}"

@pytest.mark.skipif(os.getenv("TEST_TEST_SET", "0") == "0",reason="TEST_TEST_SET not defined")
def test_accuracy(load_model):
    df_test = pd.read_csv(os.getenv("TEST_TEST_SET"))
    X_test, y_test = df_test["review"],  df_test["polarity"]
    score = load_model.score(X_test, y_test)
    print(score)
    assert load_model.score(X_test, y_test) > 0.75