import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from joblib import dump, load


# Load your CSV data into a pandas DataFrame
data = pd.read_csv('bank_cleaned.csv')

# Split the data into features and target variable
X = data.drop('deposit', axis=1)  # Assuming 'target_column' is the name of your target variable
y = data['deposit']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize your machine learning model
# Load the model
knn_model = load('knn_model.joblib')


# Make predictions on the test set
y_pred = knn_model.predict(X_test)

# Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
