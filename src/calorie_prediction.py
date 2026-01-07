"""
Calorie Prediction Module
=========================
This module implements Linear Regression to predict daily calorie
and macronutrient requirements based on user profile.
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class CaloriePredictor:
    """
    Linear Regression-based calorie and macronutrient predictor.
    
    Uses the Mifflin-St Jeor equation as baseline and adjusts
    using Linear Regression for personalized predictions.
    """
    
    def __init__(self):
        """Initialize the predictor with Linear Regression model."""
        self.model_calories = LinearRegression()
        self.model_protein = LinearRegression()
        self.model_carbs = LinearRegression()
        self.model_fat = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def calculate_bmr(self, age, gender, height_cm, weight_kg):
        """
        Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor equation.
        
        Parameters:
        -----------
        age : int
            Age in years
        gender : str
            'male' or 'female'
        height_cm : float
            Height in centimeters
        weight_kg : float
            Weight in kilograms
        
        Returns:
        --------
        float
            BMR in calories per day
        """
        # Mifflin-St Jeor Equation
        if gender.lower() == 'male':
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:  # female
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        
        return bmr
    
    def get_activity_multiplier(self, activity_level):
        """
        Get activity multiplier for Total Daily Energy Expenditure (TDEE).
        
        Parameters:
        -----------
        activity_level : str
            Activity level: 'sedentary', 'light', 'moderate', 'active', 'very_active'
        
        Returns:
        --------
        float
            Activity multiplier
        """
        multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        return multipliers.get(activity_level.lower(), 1.2)
    
    def predict_calories(self, age, gender, height_cm, weight_kg, activity_level):
        """
        Predict daily calorie requirement using Linear Regression approach.
        
        Algorithm Logic:
        ----------------
        1. Calculate BMR using Mifflin-St Jeor equation
        2. Apply activity multiplier to get TDEE
        3. Use Linear Regression to refine prediction based on user features
        
        Parameters:
        -----------
        age : int
            Age in years
        gender : str
            'male' or 'female'
        height_cm : float
            Height in centimeters
        weight_kg : float
            Weight in kilograms
        activity_level : str
            Activity level string
        
        Returns:
        --------
        float
            Predicted daily calories
        """
        # Calculate base BMR
        bmr = self.calculate_bmr(age, gender, height_cm, weight_kg)
        
        # Apply activity multiplier
        activity_mult = self.get_activity_multiplier(activity_level)
        base_tdee = bmr * activity_mult
        
        # Prepare features for Linear Regression
        # Convert gender to numeric (0 for female, 1 for male)
        gender_numeric = 1 if gender.lower() == 'male' else 0
        
        # Create feature vector
        features = np.array([[age, gender_numeric, height_cm, weight_kg, activity_mult]])
        
        if self.is_trained:
            # Use trained model for refinement
            features_scaled = self.scaler.transform(features)
            adjustment = self.model_calories.predict(features_scaled)[0]
            predicted_calories = base_tdee + adjustment
        else:
            # Use base calculation if model not trained
            predicted_calories = base_tdee
        
        # Ensure reasonable range
        predicted_calories = max(1200, min(predicted_calories, 5000))
        
        return round(predicted_calories, 2)
    
    def predict_macros(self, calories, goal='maintain'):
        """
        Predict macronutrient distribution based on calorie target.
        
        Algorithm Logic:
        ----------------
        Uses standard macronutrient ratios:
        - Protein: 20-30% of calories (4 cal/g)
        - Carbohydrates: 45-65% of calories (4 cal/g)
        - Fat: 20-35% of calories (9 cal/g)
        
        Parameters:
        -----------
        calories : float
            Daily calorie target
        goal : str
            Goal type: 'maintain', 'lose', 'gain'
        
        Returns:
        --------
        dict
            Dictionary with 'protein', 'carbs', 'fat' in grams
        """
        if goal == 'lose':
            # Higher protein, moderate carbs for weight loss
            protein_pct = 0.30
            carb_pct = 0.40
            fat_pct = 0.30
        elif goal == 'gain':
            # Higher carbs for weight gain
            protein_pct = 0.20
            carb_pct = 0.55
            fat_pct = 0.25
        else:  # maintain
            # Balanced distribution
            protein_pct = 0.25
            carb_pct = 0.45
            fat_pct = 0.30
        
        # Calculate grams (protein and carbs: 4 cal/g, fat: 9 cal/g)
        protein_grams = (calories * protein_pct) / 4
        carb_grams = (calories * carb_pct) / 4
        fat_grams = (calories * fat_pct) / 9
        
        return {
            'protein': round(protein_grams, 2),
            'carbs': round(carb_grams, 2),
            'fat': round(fat_grams, 2)
        }
    
    def train(self, X, y_calories):
        """
        Train Linear Regression model on historical data.
        
        Parameters:
        -----------
        X : np.ndarray
            Feature matrix (age, gender, height, weight, activity)
        y_calories : np.ndarray
            Target calorie values
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model_calories.fit(X_scaled, y_calories)
        self.is_trained = True

