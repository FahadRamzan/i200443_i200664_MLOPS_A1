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
from sklearn.metrics import confusion_matrix, classification_report

df = pd.read_csv('bank.csv')
df_original = pd.read_csv('bank.csv')
df.head(5)

# Check correlation between all selected columns
selected_columns = ['education', 'job', 'marital', 'age', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'deposit']

# Convert categorical columns to numeric using factorize, and then calculate correlation
correlation_matrix = df[selected_columns].apply(lambda x: x.factorize()[0]).corr()
correlation_matrix

df.dtypes
df.shape
df.info()

missing_values = df.isnull().sum()
print(missing_values)

#checking for duplicated rows
duplicated = df[df.duplicated()]
duplicated
df.describe()

# Summary of categorical columns
df.describe(include=['object'])


"""# Data Preprocessing on features

One-Hot Encoding
"""

nominal_categorical_columns = ['job', 'marital', 'education', 'contact', 'month', 'poutcome']

df_encoded = pd.get_dummies(df, columns=nominal_categorical_columns)
df = df_encoded
df.head()

all_columns = df.columns.tolist()
all_columns

binary_columns = ['default', 'housing', 'loan', 'deposit']

# Map 'yes' to 1 and 'no' to 0 for binary columns
for col in binary_columns:
    df[col] = df[col].map({'yes': 1, 'no': 0})

df.head()

df_pre = df

def detect_outliers_iqr_column(data, column_name):
    Q1 = data[column_name].quantile(0.25)
    Q3 = data[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_indices = data[(data[column_name] < lower_bound) | (data[column_name] > upper_bound)].index
    num_outliers = len(outliers_indices)
    return num_outliers, outliers_indices

def plot_outliers_scatter(data, column_name):
    plt.figure(figsize=(8, 6))
    plt.scatter(data.index, data[column_name])
    plt.title('Scatter plot of {}'.format(column_name))
    plt.xlabel('Index')
    plt.ylabel(column_name)
    plt.show()

column_name = 'age'
num_outliers, outliers_indices = detect_outliers_iqr_column(df, column_name)
print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
print("Indices of outliers:", outliers_indices)

plot_outliers_scatter(df, column_name)

column_name = 'balance'
num_outliers, outliers_indices = detect_outliers_iqr_column(df, column_name)
print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
print("Indices of outliers:", outliers_indices)

plot_outliers_scatter(df, column_name)

column_name = 'day'
num_outliers, outliers_indices = detect_outliers_iqr_column(df, column_name)
print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
print("Indices of outliers:", outliers_indices)

plot_outliers_scatter(df, column_name)

column_name = 'duration'
num_outliers, outliers_indices = detect_outliers_iqr_column(df, column_name)
print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
print("Indices of outliers:", outliers_indices)

plot_outliers_scatter(df, column_name)

column_name = 'campaign'
num_outliers, outliers_indices = detect_outliers_iqr_column(df, column_name)
print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
print("Indices of outliers:", outliers_indices)

plot_outliers_scatter(df, column_name)

column_name = 'pdays'
num_outliers, outliers_indices = detect_outliers_iqr_column(df, column_name)
print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
print("Indices of outliers:", outliers_indices)

plot_outliers_scatter(df, column_name)

column_name = 'previous'
num_outliers, outliers_indices = detect_outliers_iqr_column(df, column_name)
print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
print("Indices of outliers:", outliers_indices)

plot_outliers_scatter(df, column_name)

"""Removing Outliers"""

def remove_outliers_iqr(data, column_name):
    Q1 = data[column_name].quantile(0.25)
    Q3 = data[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_data = data[(data[column_name] >= lower_bound) & (data[column_name] <= upper_bound)]
    return filtered_data

column_name = 'age'
df = remove_outliers_iqr(df, column_name)
plot_outliers_scatter(df, column_name)

column_name = 'balance'
df = remove_outliers_iqr(df, column_name)
plot_outliers_scatter(df, column_name)

column_name = 'duration'
df = remove_outliers_iqr(df, column_name)
plot_outliers_scatter(df, column_name)

column_name = 'campaign'
df = remove_outliers_iqr(df, column_name)
plot_outliers_scatter(df, column_name)

column_name = 'pdays'
df = remove_outliers_iqr(df, column_name)
plot_outliers_scatter(df, column_name)

column_name = 'previous'
df = remove_outliers_iqr(df, column_name)
plot_outliers_scatter(df, column_name)

"""Detecting Ouliers using Z-Score"""

def detect_outliers_zscore(data, column_name, threshold=3):
    z_scores = np.abs((data[column_name] - data[column_name].mean()) / data[column_name].std())
    outliers_indices = np.where(z_scores > threshold)[0]
    num_outliers = len(outliers_indices)
    return num_outliers, outliers_indices

def remove_outliers_zscore(data, column_name, threshold=3):
    z_scores = np.abs((data[column_name] - data[column_name].mean()) / data[column_name].std())
    outliers_indices = np.where(z_scores > threshold)[0]
    data_no_outliers = data.drop(outliers_indices)
    return data_no_outliers

column_name = 'age'
threshold = 3

# Detect outliers
num_outliers, outliers_indices = detect_outliers_zscore(df_original, column_name, threshold)
print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
print("Indices of outliers:", outliers_indices)

# Remove outliers
df_no_outliers = remove_outliers_zscore(df_original, column_name, threshold)

plot_outliers_scatter(df_no_outliers, column_name)

column_name = 'balance'
threshold = 3

# Detect outliers
num_outliers, outliers_indices = detect_outliers_zscore(df_original, column_name, threshold)
print("Number of outliers in column '{}': {}".format(column_name, num_outliers))
print("Indices of outliers:", outliers_indices)

# Remove outliers
df_no_outliers = remove_outliers_zscore(df_original, column_name, threshold)

plot_outliers_scatter(df_no_outliers, column_name)

"""By only checking ouliers of two features by Z-Score, it shows that IQR was a good option.

# Data Visualization
"""

df.head()

df_original.head()

"""# Before Preprocessing"""

numerical_columns = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']

# Distribution plots (Histograms)
plt.figure(figsize=(12, 8))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(3, 3, i)
    sns.histplot(df_original[column], kde=True, color='skyblue')
    plt.title(f'Distribution of {column}')
plt.tight_layout()
plt.show()

# Box plots
plt.figure(figsize=(12, 8))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(3, 3, i)
    sns.boxplot(y=df_original[column], color='lightgreen')
    plt.title(f'Box plot of {column}')
plt.tight_layout()
plt.show()

# Correlation matrix heatmap
correlation_matrix = df_original[numerical_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
plt.show()

"""Saving cleaned data"""
df_cleaned = df

"""After Preprocessing"""
df_cleaned.head()

numerical_columns = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']

# Distribution plots (Histograms)
plt.figure(figsize=(12, 8))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(3, 3, i)
    sns.histplot(df_cleaned[column], kde=True, color='skyblue')
    plt.title(f'Distribution of {column}')
plt.tight_layout()
plt.show()

# Box plots
plt.figure(figsize=(12, 8))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(3, 3, i)
    sns.boxplot(y=df_cleaned[column], color='lightgreen')
    plt.title(f'Box plot of {column}')
plt.tight_layout()
plt.show()

# Correlation matrix heatmap
correlation_matrix = df_cleaned[numerical_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
plt.show()


"""# Data Transformation"""
# Copying the dataframe to avoid modifying the original dataframe
df_normalized = df_cleaned.copy()
df_standardized = df_cleaned.copy()

# Selecting numerical columns for normalization and standardization
numerical_cols = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']

# Normalization using Min-Max scaling
scaler = MinMaxScaler()
df_normalized[numerical_cols] = scaler.fit_transform(df_cleaned[numerical_cols])

# Standardization using Z-score scaling
scaler = StandardScaler()
df_standardized[numerical_cols] = scaler.fit_transform(df_cleaned[numerical_cols])

print("Normalized Data:")
df_normalized.head()

print("\nStandardized Data:")
df_standardized.head()

plt.figure(figsize=(16, 20))  # Keep the figure size

# Original Data
plt.subplot(3, 1, 1)
sns.histplot(data=df_cleaned[numerical_cols], kde=True, bins=20)  # Increase bins
plt.title('Original Data')

# Normalization
plt.subplot(3, 1, 2)
sns.histplot(data=df_normalized[numerical_cols], kde=True, bins=20)  # Increase bins
plt.title('Normalized Data')

# Standardization
plt.subplot(3, 1, 3)
sns.histplot(data=df_standardized[numerical_cols], kde=True, bins=20)  # Increase bins
plt.title('Standardized Data')


plt.tight_layout()
plt.show()

"""# Classification"""

# Convert dataframe to numpy array
X = df_pre.drop(columns=['deposit']).values  # Features
y = df_pre['deposit'].values  # Target variable

# Splitting the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing classifiers
classifiers = {
    'KNN': KNeighborsClassifier(),
    'SVM': SVC(),
    'Naive Bayes': GaussianNB(),
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': DecisionTreeClassifier()
}

# Training and evaluating each classifier
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

# Convert dataframe to numpy array
X = df_cleaned.drop(columns=['deposit']).values  # Features
y = df_cleaned['deposit'].values  # Target variable

# Splitting the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing classifiers
classifiers = {
    'KNN': KNeighborsClassifier(),
    'SVM': SVC(),
    'Naive Bayes': GaussianNB(),
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': DecisionTreeClassifier()
}

# Training and evaluating each classifier
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

# Convert dataframe to numpy array
X = df_standardized.drop(columns=['deposit']).values  # Features
y = df_standardized['deposit'].values  # Target variable

# Splitting the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing classifiers
classifiers = {
    'KNN': KNeighborsClassifier(),
    'SVM': SVC(),
    'Naive Bayes': GaussianNB(),
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': DecisionTreeClassifier()
}

# Training and evaluating each classifier
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

# Convert dataframe to numpy array
X = df_normalized.drop(columns=['deposit']).values  # Features
y = df_normalized['deposit'].values  # Target variable

# Splitting the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing classifiers
classifiers = {
    'KNN': KNeighborsClassifier(),
    'SVM': SVC(),
    'Naive Bayes': GaussianNB(),
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': DecisionTreeClassifier()
}

# Training and evaluating each classifier
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