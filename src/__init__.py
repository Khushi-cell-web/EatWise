"""
EatWise - Personalized Nutrition & Meal Recommendation System
==============================================================

A Python-based AI coursework project demonstrating:
- Linear Regression for calorie prediction
- K-Nearest Neighbors for food recommendations
- Greedy Algorithm for meal planning
"""

__version__ = "1.0.0"

from .data_loader import load_nutrition_data, preprocess_data
from .calorie_prediction import CaloriePredictor
from .food_recommendation import FoodRecommender
from .meal_planner import MealPlanner

__all__ = [
    'load_nutrition_data',
    'preprocess_data',
    'CaloriePredictor',
    'FoodRecommender',
    'MealPlanner'
]

