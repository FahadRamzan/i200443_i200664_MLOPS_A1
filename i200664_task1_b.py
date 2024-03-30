import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


# Load the dataset
df = pd.read_csv('bank.csv')
df_original = pd.read_csv('bank.csv')

# Display the first 5 rows
print(df.head(5))

# Check correlation between selected columns
selected_columns = [
    'education', 'job', 'marital', 'age', 'default', 'balance', 'housing',
    'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays',
    'previous', 'poutcome', 'deposit'
]
correlation_matrix = df[selected_columns].corr()
print(correlation_matrix)

# Display data types, shape, and info
print(df.dtypes)
print(df.shape)
print(df.info())

# Check for missing values
missing_values = df.isnull().sum()
print(missing_values)

# Check for duplicated rows
duplicated = df[df.duplicated()]
print(duplicated)
print(df.describe())

# Summary of categorical columns
print(df.describe(include=['object']))

# Data Preprocessing on features

# One-Hot Encoding
nominal_categorical_columns = [
    'job', 'marital', 'education', 'contact', 'month', 'poutcome'
]
df_encoded = pd.get_dummies(df, columns=nominal_categorical_columns)
df = df_encoded

# Map 'yes' to 1 and 'no' to 0 for binary columns
binary_columns = ['default', 'housing', 'loan', 'deposit']
for col in binary_columns:
    df[col] = df[col].map({'yes': 1, 'no': 0})

# Save preprocessed data
df_pre = df.copy()

# Function to detect outliers using IQR
def detect_outliers_iqr_column(data, column_name):
    Q1 = data[column_name].quantile(0.25)
    Q3 = data[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_indices = (
        data[
            (data[column_name] < lower_bound) |
            (data[column_name] > upper_bound)
        ].index
    )
    num_outliers = len(outliers_indices)
    return num_outliers, outliers_indices


# Function to remove outliers using IQR
def remove_outliers_iqr(data, column_name):
    Q1 = data[column_name].quantile(0.25)
    Q3 = data[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_data = (
        data[
            (data[column_name] >= lower_bound) & 
            (data[column_name] <= upper_bound)
        ]
    )
    return filtered_data


# Detect and remove outliers for selected numerical columns
numerical_columns = [
    'age', 'balance', 'duration', 'campaign', 'pdays', 'previous'
]
for column_name in numerical_columns:
    num_outliers, outliers_indices = detect_outliers_iqr_column(df, column_name)
    print("Indices of outliers:", outliers_indices)
    df = remove_outliers_iqr(df, column_name)

# Detect outliers using Z-Score
def detect_outliers_zscore(data, column_name, threshold=3):
    z_scores = np.abs(
        (data[column_name] - data[column_name].mean()) /
        data[column_name].std()
    )
    outliers_indices = np.where(z_scores > threshold)[0]
    num_outliers = len(outliers_indices)
    return num_outliers, outliers_indices


# Remove outliers using Z-Score
def remove_outliers_zscore(data, column_name, threshold=3):
    z_scores = np.abs(
        (data[column_name] - data[column_name].mean()) /
        data[column_name].std()
    )
    outliers_indices = np.where(z_scores > threshold)[0]
    data_no_outliers = data.drop(outliers_indices)
    return data_no_outliers


for column_name in numerical_columns:
    num_outliers, outliers_indices = detect_outliers_zscore(df_original, column_name)
    print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
    print("Indices of outliers:", outliers_indices)
    df_no_outliers = remove_outliers_zscore(df_original, column_name)
    # plot_outliers_scatter(df_no_outliers, column_name)

# Data Visualization

# Distribution plots and Box plots before preprocessing
numerical_columns = [
    'age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous'
]
plt.figure(figsize=(12, 8))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(3, 3, i)
    sns.histplot(df_original[column], kde=True, color='skyblue')
    plt.title(f'Distribution of {column}')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(3, 3, i)
    sns.boxplot(y=df_original[column], color='lightgreen')
    plt.title(f'Box plot of {column}')
plt.tight_layout()
plt.show()

# Correlation matrix heatmap before preprocessing
correlation_matrix = df_original[numerical_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap='coolwarm',
    fmt=".2f",
    linewidths=0.5
)
plt.title('Correlation Matrix Heatmap')
plt.show()

# Data Transformation

# Normalization using Min-Max scaling
scaler = MinMaxScaler()
df_normalized = df_cleaned.copy()
df_normalized[numerical_columns] = scaler.fit_transform(
    df_cleaned[numerical_columns]
)


# Standardization using Z-score scaling
scaler = StandardScaler()
df_standardized = df_cleaned.copy()
df_standardized[numerical_columns] = scaler.fit_transform(
    df_cleaned[numerical_columns]
)

# Display histograms for original, normalized, and standardized data
plt.figure(figsize=(16, 20))  # Keep the figure size
plt.subplot(3, 1, 1)
sns.histplot(data=df_cleaned[numerical_columns], kde=True, bins=20)
plt.title('Original Data')

plt.subplot(3, 1, 2)
sns.histplot(data=df_normalized[numerical_columns], kde=True, bins=20)
plt.title('Normalized Data')

plt.subplot(3, 1, 3)
sns.histplot(data=df_standardized[numerical_columns], kde=True, bins=20)
plt.title('Standardized Data')

plt.tight_layout()
plt.show()

# Classification

# Convert dataframe to numpy array
X = df_pre.drop(columns=['deposit']).values  # Features
y = df_pre['deposit'].values  # Target variable

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize classifiers
classifiers = {
    'KNN': KNeighborsClassifier(),
    'SVM': SVC(),
    'Naive Bayes': GaussianNB(),
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': DecisionTreeClassifier()
}

# Train and evaluate each classifier
for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'{name}: Accuracy = {accuracy:.2f}')

    cm = confusion_matrix(y_test, y_pred)
    print(f'Confusion matrix for {name}:')
    print(cm)
    print(classification_report(y_test, y_pred))
    print("\n")
