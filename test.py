import pytest
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from joblib import load


@pytest.fixture
def trained_model():
    # Load the trained model from the file
    knn_model = load('knn_model.joblib')
    return knn_model

@pytest.fixture
def test_data():
    # Load test data
    data = pd.read_csv('bank_cleaned.csv')
    X_test = data.drop('deposit', axis=1)
    y_test = data['deposit']
    return X_test, y_test

def test_accuracy(trained_model, test_data):
    knn_model = trained_model
    X_test, y_test = test_data
    # Make predictions
    y_pred = knn_model.predict(X_test)
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    # Check if accuracy is not None and between 0 and 1
    assert accuracy is not None
    assert 0 <= accuracy <= 1

