import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import pickle
import os

# Dataset
data = pd.read_csv("app/models/insurance_processed.csv")
# DATA_PATH = os.path.join(os.path.dirname(__file__), "insurance_processed.csv")

df = pd.DataFrame(data)

# Define features and target
X = df.drop(columns=['charges'])
y = df['charges']

# Label encode categorical columns
label_encoder = LabelEncoder()
X['sex'] = label_encoder.fit_transform(X['sex'])
X['smoker'] = label_encoder.fit_transform(X['smoker'])
X['region'] = label_encoder.fit_transform(X['region'])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline for preprocessing and model
pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Fit the model
pipeline.fit(X_train, y_train)

# Save the model to disk
with open('app/models/insurance_model.pkl', 'wb') as model_file:
    pickle.dump(pipeline, model_file)

print("Model trained and saved successfully!")