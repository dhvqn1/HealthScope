"""
Train all ML models for HealthScope
"""

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def train_heart_model():
    """Train Heart Disease prediction model"""
    print("Training Heart Disease Model...")
    data = pd.read_csv('data/heart_disease.csv')
    
    X = data.drop('target', axis=1)
    y = data['target']
    
    feature_names = X.columns.tolist()
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Heart Disease Model Accuracy: {accuracy:.4f}")
    
    with open('models_pkls/heart_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('models_pkls/heart_features.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    
    return model, accuracy


def train_diabetes_model():
    """Train Diabetes prediction model"""
    print("\nTraining Diabetes Model...")
    data = pd.read_csv('data/diabetes.csv')
    
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']
    
    feature_names = X.columns.tolist()
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Diabetes Model Accuracy: {accuracy:.4f}")
    
    with open('models_pkls/diabetes_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('models_pkls/diabetes_features.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    
    return model, accuracy


if __name__ == "__main__":
    print("="*60)
    print("Training All HealthScope Models")
    print("="*60)
    
    heart_model, heart_acc = train_heart_model()
    diabetes_model, diabetes_acc = train_diabetes_model()
    
    print("\n" + "="*60)
    print("Training Complete!")
    print(f"Heart Disease Accuracy: {heart_acc:.4f}")
    print(f"Diabetes Accuracy: {diabetes_acc:.4f}")
    print("="*60)
