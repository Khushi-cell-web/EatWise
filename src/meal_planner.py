"""
Meal Planner Module
===================
This module implements a Greedy Algorithm to generate optimal
daily meal plans (breakfast, lunch, dinner) based on nutritional targets.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple


class MealPlanner:
    """
    Greedy Algorithm-based meal planner.
    
    Algorithm Logic:
    ----------------
    1. Start with empty meal plan
    2. For each meal (breakfast, lunch, dinner):
       a. Calculate remaining nutritional needs
       b. Find food that best fits remaining needs (greedy choice)
       c. Add food to meal plan
       d. Update remaining nutritional needs
    3. Repeat until all meals are planned or target is reached
    
    Greedy Strategy:
    - At each step, select the food that minimizes the difference
      between current nutritional state and target
    """
    
    def __init__(self, food_data):
        """
        Initialize meal planner with food dataset.
        
        Parameters:
        -----------
        food_data : pd.DataFrame
            DataFrame containing food items and nutritional values
        """
        self.food_data = food_data.copy()
        self.nutrition_cols = ['calories', 'carbohydrates', 'protein', 'fat', 'fiber']
    
    def calculate_nutritional_gap(self, current_nutrition, target_nutrition):
        """
        Calculate how far current nutrition is from target.
        
        Parameters:
        -----------
        current_nutrition : dict
            Current nutritional values
        target_nutrition : dict
            Target nutritional values
        
        Returns:
        --------
        float
            Total normalized gap score (lower is better)
        """
        gap = 0
        
        # Weighted gap calculation (calories most important)
        weights = {'calories': 0.4, 'protein': 0.25, 'carbohydrates': 0.15, 'fat': 0.15, 'fiber': 0.05}
        
        for nutrient in self.nutrition_cols:
            if nutrient in target_nutrition and target_nutrition[nutrient] > 0:
                current_val = current_nutrition.get(nutrient, 0)
                target_val = target_nutrition[nutrient]
                
                # Normalized gap (avoid division by zero)
                if target_val > 0:
                    normalized_gap = abs(current_val - target_val) / target_val
                    gap += weights.get(nutrient, 0.1) * normalized_gap
        
        return gap
    
    def find_best_food(self, remaining_needs, meal_type='any', exclude_foods=None):
        """
        Greedy selection: Find the food that best fits remaining nutritional needs.
        
        Parameters:
        -----------
        remaining_needs : dict
            Remaining nutritional requirements
        meal_type : str
            Meal type filter: 'breakfast', 'lunch', 'dinner', 'any'
        exclude_foods : list, optional
            List of food names to exclude
        
        Returns:
        --------
        pd.Series
            Best matching food item
        """
        if exclude_foods is None:
            exclude_foods = []
        
        # Filter foods
        available_foods = self.food_data[~self.food_data['food_name'].isin(exclude_foods)].copy()
        
        if len(available_foods) == 0:
            return None
        
        # Calculate gap for each food
        best_food = None
        best_gap = float('inf')
        
        for idx, food in available_foods.iterrows():
            # Calculate nutrition if this food is added
            food_nutrition = {col: food[col] for col in self.nutrition_cols if col in food}
            
            # Calculate gap
            gap = self.calculate_nutritional_gap(food_nutrition, remaining_needs)
            
            if gap < best_gap:
                best_gap = gap
                best_food = food
        
        return best_food
    
    def generate_meal_plan(self, target_calories, target_protein, target_carbs, target_fat, 
                          target_fiber=25, meal_distribution=None):
        """
        Generate optimal daily meal plan using Greedy Algorithm.
        
        Algorithm Steps:
        ----------------
        1. Initialize meal plan and remaining needs
        2. For each meal (breakfast, lunch, dinner):
           a. Calculate meal-specific targets (based on distribution)
           b. Greedily select foods that minimize nutritional gap
           c. Add to meal plan
           d. Update remaining needs
        3. Return complete meal plan
        
        Parameters:
        -----------
        target_calories : float
            Daily calorie target
        target_protein : float
            Daily protein target (grams)
        target_carbs : float
            Daily carbohydrate target (grams)
        target_fat : float
            Daily fat target (grams)
        target_fiber : float
            Daily fiber target (grams, default: 25)
        meal_distribution : dict, optional
            Distribution of calories across meals. Default: {'breakfast': 0.25, 'lunch': 0.40, 'dinner': 0.35}
        
        Returns:
        --------
        dict
            Dictionary with meal plans and nutritional summary
        """
        # Default meal distribution
        if meal_distribution is None:
            meal_distribution = {
                'breakfast': 0.25,  # 25% of daily calories
                'lunch': 0.40,      # 40% of daily calories
                'dinner': 0.35      # 35% of daily calories
            }
        
        # Initialize meal plan
        meal_plan = {
            'breakfast': [],
            'lunch': [],
            'dinner': []
        }
        
        # Calculate meal-specific targets
        meal_targets = {}
        for meal, pct in meal_distribution.items():
            meal_targets[meal] = {
                'calories': target_calories * pct,
                'protein': target_protein * pct,
                'carbohydrates': target_carbs * pct,
                'fat': target_fat * pct,
                'fiber': target_fiber * pct
            }
        
        # Track selected foods to avoid duplicates
        selected_foods = []
        
        # Greedy algorithm: plan each meal
        for meal_name in ['breakfast', 'lunch', 'dinner']:
            remaining_needs = meal_targets[meal_name].copy()
            meal_foods = []
            
            # Try to fill meal with 1-3 foods (greedy selection)
            max_foods_per_meal = 3
            for _ in range(max_foods_per_meal):
                # Find best food for remaining needs
                best_food = self.find_best_food(remaining_needs, meal_type=meal_name, exclude_foods=selected_foods)
                
                if best_food is None:
                    break
                
                # Check if adding this food would exceed meal target significantly
                food_calories = best_food.get('calories', 0)
                if food_calories > remaining_needs['calories'] * 1.5:  # Don't exceed by more than 50%
                    break
                
                # Add food to meal
                meal_foods.append({
                    'food_name': best_food['food_name'],
                    'calories': best_food.get('calories', 0),
                    'protein': best_food.get('protein', 0),
                    'carbohydrates': best_food.get('carbohydrates', 0),
                    'fat': best_food.get('fat', 0),
                    'fiber': best_food.get('fiber', 0)
                })
                
                # Update remaining needs
                for nutrient in self.nutrition_cols:
                    if nutrient in remaining_needs:
                        remaining_needs[nutrient] -= best_food.get(nutrient, 0)
                        remaining_needs[nutrient] = max(0, remaining_needs[nutrient])  # Don't go negative
                
                # Mark food as selected
                selected_foods.append(best_food['food_name'])
                
                # Stop if we've met most of the meal target
                if remaining_needs['calories'] < meal_targets[meal_name]['calories'] * 0.2:
                    break
            
            meal_plan[meal_name] = meal_foods
        
        # Calculate actual nutrition achieved
        total_nutrition = self._calculate_total_nutrition(meal_plan)
        
        return {
            'meal_plan': meal_plan,
            'total_nutrition': total_nutrition,
            'target_nutrition': {
                'calories': target_calories,
                'protein': target_protein,
                'carbohydrates': target_carbs,
                'fat': target_fat,
                'fiber': target_fiber
            }
        }
    
    def _calculate_total_nutrition(self, meal_plan):
        """Calculate total nutrition from meal plan."""
        total = {col: 0 for col in self.nutrition_cols}
        
        for meal_name, foods in meal_plan.items():
            for food in foods:
                for nutrient in self.nutrition_cols:
                    if nutrient in food:
                        total[nutrient] += food[nutrient]
        
        return total

