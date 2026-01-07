"""
Food Recommendation Module
==========================
This module implements K-Nearest Neighbors (KNN) algorithm to find
nutritionally similar foods and make recommendations.
"""

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pandas as pd


class FoodRecommender:
    """
    K-Nearest Neighbors-based food recommendation system.
    
    Algorithm Logic:
    ----------------
    1. Represent each food as a feature vector (calories, protein, carbs, fat, fiber)
    2. Normalize features using StandardScaler
    3. Use KNN to find foods with similar nutritional profiles
    4. Return top K most similar foods
    """
    
    def __init__(self, n_neighbors=5):
        """
        Initialize the KNN-based food recommender.
        
        Parameters:
        -----------
        n_neighbors : int
            Number of nearest neighbors to find (default: 5)
        """
        self.n_neighbors = n_neighbors
        self.knn_model = NearestNeighbors(n_neighbors=n_neighbors + 1, metric='euclidean')
        self.scaler = StandardScaler()
        self.food_data = None
        self.feature_matrix = None
        self.is_fitted = False
    
    def fit(self, food_data, feature_cols=None):
        """
        Fit the KNN model on the food dataset.
        
        Parameters:
        -----------
        food_data : pd.DataFrame
            DataFrame containing food items and their nutritional values
        feature_cols : list, optional
            List of column names to use as features. If None, uses default.
        """
        self.food_data = food_data.copy()
        
        # Default feature columns
        if feature_cols is None:
            feature_cols = ['calories', 'carbohydrates', 'protein', 'fat', 'fiber']
        
        # Extract feature matrix
        self.feature_matrix = food_data[feature_cols].values
        
        # Normalize features (important for KNN with different scales)
        self.feature_matrix_scaled = self.scaler.fit_transform(self.feature_matrix)
        
        # Fit KNN model
        self.knn_model.fit(self.feature_matrix_scaled)
        self.is_fitted = True
    
    def find_similar_foods(self, target_food_name=None, target_nutrition=None, n_recommendations=5):
        """
        Find nutritionally similar foods using KNN algorithm.
        
        Algorithm Steps:
        ----------------
        1. If target_food_name provided: extract its nutrition profile
        2. If target_nutrition provided: use it directly
        3. Normalize target nutrition vector
        4. Find K nearest neighbors using Euclidean distance
        5. Return similar foods with their similarity scores
        
        Parameters:
        -----------
        target_food_name : str, optional
            Name of the food to find similar items for
        target_nutrition : dict or np.ndarray, optional
            Target nutrition profile: {'calories': x, 'protein': y, ...}
        n_recommendations : int
            Number of recommendations to return
        
        Returns:
        --------
        pd.DataFrame
            DataFrame with similar foods and their nutritional values
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making recommendations")
        
        # Get target nutrition vector
        if target_food_name:
            # Find food in dataset
            food_idx = self.food_data[self.food_data['food_name'].str.lower() == target_food_name.lower()].index
            
            if len(food_idx) == 0:
                raise ValueError(f"Food '{target_food_name}' not found in dataset")
            
            target_idx = food_idx[0]
            target_vector = self.feature_matrix[target_idx:target_idx+1]
        
        elif target_nutrition:
            # Convert dict to array if needed
            if isinstance(target_nutrition, dict):
                feature_cols = ['calories', 'carbohydrates', 'protein', 'fat', 'fiber']
                target_vector = np.array([[target_nutrition.get(col, 0) for col in feature_cols]])
            else:
                target_vector = target_nutrition.reshape(1, -1) if target_nutrition.ndim == 1 else target_nutrition
        else:
            raise ValueError("Either target_food_name or target_nutrition must be provided")
        
        # Normalize target vector
        target_scaled = self.scaler.transform(target_vector)
        
        # Find nearest neighbors
        distances, indices = self.knn_model.kneighbors(target_scaled, n_neighbors=min(n_recommendations + 1, len(self.food_data)))
        
        # Get similar foods (exclude the food itself if it was in dataset)
        similar_indices = indices[0][1:]  # Skip first (might be the same food)
        similar_distances = distances[0][1:]
        
        # Create results DataFrame
        results = self.food_data.iloc[similar_indices].copy()
        results['similarity_score'] = 1 / (1 + similar_distances)  # Convert distance to similarity (0-1 scale)
        results = results.sort_values('similarity_score', ascending=False)
        
        return results[['food_name', 'calories', 'carbohydrates', 'protein', 'fat', 'fiber', 'similarity_score']]
    
    def recommend_by_macros(self, target_protein, target_carbs, target_fat, target_calories=None, n_recommendations=5):
        """
        Recommend foods based on target macronutrient profile.
        
        Parameters:
        -----------
        target_protein : float
            Target protein in grams
        target_carbs : float
            Target carbohydrates in grams
        target_fat : float
            Target fat in grams
        target_calories : float, optional
            Target calories. If None, calculated from macros.
        n_recommendations : int
            Number of recommendations
        
        Returns:
        --------
        pd.DataFrame
            Recommended foods matching the macro profile
        """
        # Calculate calories if not provided
        if target_calories is None:
            target_calories = target_protein * 4 + target_carbs * 4 + target_fat * 9
        
        target_nutrition = {
            'calories': target_calories,
            'carbohydrates': target_carbs,
            'protein': target_protein,
            'fat': target_fat,
            'fiber': 0  # Not specified, use 0
        }
        
        return self.find_similar_foods(target_nutrition=target_nutrition, n_recommendations=n_recommendations)

