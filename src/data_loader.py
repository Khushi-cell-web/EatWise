"""
Data Loader Module
==================
This module handles loading and preprocessing the nutrition dataset.
Suitable for academic coursework demonstration.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_nutrition_data(file_path=None):
    """
    Load the nutrition dataset from CSV file.
    
    Parameters:
    -----------
    file_path : str, optional
        Path to the CSV file. If None, uses default path.
    
    Returns:
    --------
    pd.DataFrame
        Preprocessed nutrition dataset with standardized column names.
    """
    if file_path is None:
        # Default path relative to project root
        project_root = Path(__file__).parent.parent
        file_path = project_root / "data" / "foods_nutrition.csv"
    
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Standardize column names (handle variations in dataset)
    column_mapping = {
        'Food Items': 'food_name',
        'Energy kcal': 'calories',
        'Carbs': 'carbohydrates',
        'Protein(g)': 'protein',
        'Fat(g)': 'fat',
        'Fibre(g)': 'fiber',
        'Freesugar(g)': 'sugar',
        'Cholestrol(mg)': 'cholesterol',
        'Calcium(mg)': 'calcium'
    }
    
    # Rename columns if they exist
    df = df.rename(columns=column_mapping)
    
    # Ensure required columns exist
    required_cols = ['food_name', 'calories', 'carbohydrates', 'protein', 'fat', 'fiber']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Fill missing values with 0 for nutritional values
    nutritional_cols = ['calories', 'carbohydrates', 'protein', 'fat', 'fiber']
    for col in nutritional_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Remove rows with invalid data (negative values or zero calories)
    df = df[df['calories'] > 0].copy()
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    return df


def preprocess_data(df):
    """
    Additional preprocessing steps for the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw nutrition dataset
    
    Returns:
    --------
    pd.DataFrame
        Preprocessed dataset ready for ML algorithms
    """
    # Create a copy to avoid modifying original
    processed_df = df.copy()
    
    # Ensure all nutritional values are non-negative
    nutritional_cols = ['calories', 'carbohydrates', 'protein', 'fat', 'fiber']
    for col in nutritional_cols:
        if col in processed_df.columns:
            processed_df[col] = processed_df[col].clip(lower=0)
    
    # Calculate macronutrient percentages (useful for similarity)
    processed_df['protein_pct'] = (processed_df['protein'] * 4 / processed_df['calories'] * 100).fillna(0)
    processed_df['carb_pct'] = (processed_df['carbohydrates'] * 4 / processed_df['calories'] * 100).fillna(0)
    processed_df['fat_pct'] = (processed_df['fat'] * 9 / processed_df['calories'] * 100).fillna(0)
    
    # Clip percentages to reasonable ranges
    processed_df['protein_pct'] = processed_df['protein_pct'].clip(0, 100)
    processed_df['carb_pct'] = processed_df['carb_pct'].clip(0, 100)
    processed_df['fat_pct'] = processed_df['fat_pct'].clip(0, 100)
    
    return processed_df


def get_nutrition_features(df):
    """
    Extract feature matrix for ML algorithms.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed nutrition dataset
    
    Returns:
    --------
    np.ndarray
        Feature matrix with nutritional values
    """
    feature_cols = ['calories', 'carbohydrates', 'protein', 'fat', 'fiber']
    features = df[feature_cols].values
    return features

