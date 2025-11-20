"""
PCOS Model Training Script
Trains a RandomForest classifier on PCOS data and saves the model
"""

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def train_pcos_model():
    """Train PCOS prediction model and save to pickle file"""
    
    print("Loading PCOS data...")
    data = pd.read_csv('data/pcos_data.csv')
    
    print(f"Dataset shape: {data.shape}")
    print(f"Columns: {data.columns.tolist()}")
    
    # Prepare features and target
    # Convert Risk column to binary (Yes/No to 1/0)
    y = (data['Risk'] == 'Yes').astype(int)
    
    # Drop target and non-predictive columns
    X = data.drop(['Risk', 'Country'], axis=1, errors='ignore')
    
    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    print(f"\nCategorical columns: {categorical_cols}")
    print(f"Numerical columns: {numerical_cols}")
    
    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ])
    
    # Create the full pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ))
    ])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set size: {X_train.shape}")
    print(f"Test set size: {X_test.shape}")
    
    # Train the model
    print("\nTraining PCOS model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    train_score = pipeline.score(X_train, y_train)
    test_score = pipeline.score(X_test, y_test)
    
    print(f"\nTraining accuracy: {train_score:.4f}")
    print(f"Test accuracy: {test_score:.4f}")
    
    # Save the model
    model_path = 'models_pkls/pcos_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
    
    print(f"\nModel saved to {model_path}")
    
    # Save feature names for later use
    feature_info = {
        'categorical_features': categorical_cols,
        'numerical_features': numerical_cols,
        'all_features': X.columns.tolist()
    }
    
    with open('models_pkls/pcos_features.pkl', 'wb') as f:
        pickle.dump(feature_info, f)
    
    print("Feature information saved")
    
    return pipeline, test_score


if __name__ == "__main__":
    model, accuracy = train_pcos_model()
    print(f"\n{'='*50}")
    print(f"PCOS Model Training Complete!")
    print(f"Final Test Accuracy: {accuracy:.4f}")
    print(f"{'='*50}")
