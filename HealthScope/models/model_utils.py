"""
Model Utilities for HealthScope
Functions for loading models and making predictions with unified risk assessment
"""

import pickle
import pandas as pd
import numpy as np
import streamlit as st


@st.cache_resource
def load_heart_model():
    """Load the trained heart disease model"""
    try:
        with open('models_pkls/heart_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('models_pkls/heart_features.pkl', 'rb') as f:
            features = pickle.load(f)
        return model, features
    except Exception as e:
        st.error(f"Error loading heart model: {e}")
        return None, None


@st.cache_resource
def load_diabetes_model():
    """Load the trained diabetes model"""
    try:
        with open('models_pkls/diabetes_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('models_pkls/diabetes_features.pkl', 'rb') as f:
            features = pickle.load(f)
        return model, features
    except Exception as e:
        st.error(f"Error loading diabetes model: {e}")
        return None, None


@st.cache_resource
def load_pcos_model():
    """Load the trained PCOS model"""
    try:
        with open('models_pkls/pcos_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Error loading PCOS model: {e}")
        return None


@st.cache_resource
def load_pcos_features():
    """Load PCOS feature information"""
    try:
        with open('models_pkls/pcos_features.pkl', 'rb') as f:
            features = pickle.load(f)
        return features
    except Exception as e:
        return None


def get_risk_classification(probability):
    """
    Convert probability to risk classification
    
    Args:
        probability: Risk probability (0-1)
    
    Returns:
        tuple: (risk_level, color, recommendation)
    """
    if probability < 0.33:
        return "Low Risk", "#10B981", "Maintain healthy lifestyle and regular check-ups."
    elif probability < 0.67:
        return "Moderate Risk", "#F59E0B", "Consult healthcare provider and consider lifestyle modifications."
    else:
        return "High Risk", "#EF4444", "Immediate medical consultation recommended."


def predict_heart_disease(model, features, input_data):
    """
    Predict heart disease risk
    
    Args:
        model: Trained model
        features: List of feature names
        input_data: Dictionary with input features
    
    Returns:
        dict: Prediction results with risk classification
    """
    try:
        # Create DataFrame with correct feature order
        df = pd.DataFrame([input_data])[features]
        
        # Make prediction
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]
        
        # Get risk classification
        risk_level, color, recommendation = get_risk_classification(probability)
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': risk_level,
            'color': color,
            'recommendation': recommendation,
            'success': True
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def predict_diabetes(model, features, input_data):
    """
    Predict diabetes risk
    
    Args:
        model: Trained model
        features: List of feature names
        input_data: Dictionary with input features
    
    Returns:
        dict: Prediction results with risk classification
    """
    try:
        # Create DataFrame with correct feature order
        df = pd.DataFrame([input_data])[features]
        
        # Make prediction
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]
        
        # Get risk classification
        risk_level, color, recommendation = get_risk_classification(probability)
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': risk_level,
            'color': color,
            'recommendation': recommendation,
            'success': True
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def predict_pcos(model, input_data):
    """
    Predict PCOS risk
    
    Args:
        model: Trained pipeline model
        input_data: Dictionary with input features
    
    Returns:
        dict: Prediction results with risk classification
    """
    try:
        # Create DataFrame from input
        df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]
        
        # Get risk classification
        risk_level, color, recommendation = get_risk_classification(probability)
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': risk_level,
            'color': color,
            'recommendation': recommendation,
            'success': True
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_feature_importance(model, feature_names, top_n=10):
    """
    Extract feature importance from model
    
    Args:
        model: Trained model with feature_importances_
        feature_names: List of feature names
        top_n: Number of top features to return
    
    Returns:
        List of (feature_name, importance) tuples
    """
    try:
        # Handle pipeline models
        if hasattr(model, 'named_steps'):
            classifier = model.named_steps.get('classifier', model)
        else:
            classifier = model
        
        # Get feature importances
        if hasattr(classifier, 'feature_importances_'):
            importances = classifier.feature_importances_
            
            # Handle transformed feature names from pipeline
            if hasattr(model, 'named_steps') and 'preprocessor' in model.named_steps:
                try:
                    transformed_names = model.named_steps['preprocessor'].get_feature_names_out()
                    feature_names = transformed_names
                except:
                    pass
            
            # Ensure we have the right number of feature names
            if len(feature_names) != len(importances):
                feature_names = [f"Feature_{i}" for i in range(len(importances))]
            
            # Create list of (feature, importance) tuples and sort
            importance_list = list(zip(feature_names, importances))
            importance_list.sort(key=lambda x: x[1], reverse=True)
            
            return importance_list[:top_n]
        else:
            return []
    except Exception as e:
        return []
