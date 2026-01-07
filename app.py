"""
EatWise - Web UI Application
============================
Streamlit-based web interface for the EatWise nutrition recommendation system.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add src to path
current_dir = os.getcwd()
src_path = os.path.join(current_dir, 'src')
if os.path.exists(src_path):
    sys.path.insert(0, src_path)

from data_loader import load_nutrition_data, preprocess_data
from calorie_prediction import CaloriePredictor
from food_recommendation import FoodRecommender
from meal_planner import MealPlanner

# Page configuration
st.set_page_config(
    page_title="EatWise - Nutrition Recommendation System",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #A23B72;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🍎 EatWise</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">Personalized Nutrition & Meal Recommendation System</h2>', unsafe_allow_html=True)

# Sidebar for user input
st.sidebar.header("👤 User Profile")

# Load data once
@st.cache_data
def load_data():
    """Load and cache the nutrition dataset."""
    data_path = os.path.join(current_dir, 'data', 'foods_nutrition.csv')
    df_raw = load_nutrition_data(data_path)
    df = preprocess_data(df_raw)
    return df

# Load dataset
try:
    df = load_data()
    st.sidebar.success(f"✅ Dataset loaded: {len(df)} foods")
except Exception as e:
    st.sidebar.error(f"❌ Error loading dataset: {e}")
    st.stop()

# User input form
with st.sidebar.form("user_profile"):
    age = st.number_input("Age (years)", min_value=10, max_value=100, value=25, step=1)
    gender = st.selectbox("Gender", ["male", "female"])
    height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=175, step=1)
    weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70, step=1)
    activity_level = st.selectbox(
        "Activity Level",
        ["sedentary", "light", "moderate", "active", "very_active"],
        index=2
    )
    goal = st.selectbox("Goal", ["maintain", "lose", "gain"], index=0)
    
    submitted = st.form_submit_button("🚀 Generate Recommendations", use_container_width=True)

# Main content area
if submitted:
    # Initialize predictor
    predictor = CaloriePredictor()
    
    # Predict calories and macros
    predicted_calories = predictor.predict_calories(
        age=age,
        gender=gender,
        height_cm=height_cm,
        weight_kg=weight_kg,
        activity_level=activity_level
    )
    
    predicted_macros = predictor.predict_macros(predicted_calories, goal=goal)
    
    # Display predictions
    st.header("📊 Your Daily Nutritional Requirements")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Calories", f"{predicted_calories:.0f} kcal")
    with col2:
        st.metric("Protein", f"{predicted_macros['protein']:.1f} g")
    with col3:
        st.metric("Carbohydrates", f"{predicted_macros['carbs']:.1f} g")
    with col4:
        st.metric("Fat", f"{predicted_macros['fat']:.1f} g")
    
    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Pie chart
    macros_cal = [
        predicted_macros['protein'] * 4,
        predicted_macros['carbs'] * 4,
        predicted_macros['fat'] * 9
    ]
    ax1.pie(macros_cal, labels=['Protein', 'Carbs', 'Fat'], autopct='%1.1f%%', startangle=90)
    ax1.set_title('Calorie Distribution')
    
    # Bar chart
    macros_g = [predicted_macros['protein'], predicted_macros['carbs'], predicted_macros['fat']]
    ax2.bar(['Protein', 'Carbs', 'Fat'], macros_g, color=['#FF6B6B', '#4ECDC4', '#FFE66D'])
    ax2.set_title('Macronutrient Requirements (grams)')
    ax2.set_ylabel('Grams')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Food Recommendations
    st.header("🍽️ Recommended Foods")
    
    # Initialize recommender
    recommender = FoodRecommender(n_neighbors=10)
    recommender.fit(df)
    
    # Get recommendations
    recommended_foods = recommender.recommend_by_macros(
        target_protein=predicted_macros['protein'],
        target_carbs=predicted_macros['carbs'],
        target_fat=predicted_macros['fat'],
        target_calories=predicted_calories,
        n_recommendations=10
    )
    
    # Display recommendations
    st.subheader("Top 10 Foods Matching Your Macro Profile")
    display_cols = ['food_name', 'calories', 'protein', 'carbohydrates', 'fat', 'similarity_score']
    st.dataframe(
        recommended_foods[display_cols].rename(columns={
            'food_name': 'Food Name',
            'calories': 'Calories',
            'protein': 'Protein (g)',
            'carbohydrates': 'Carbs (g)',
            'fat': 'Fat (g)',
            'similarity_score': 'Similarity Score'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Meal Plan Generation
    st.header("📅 Your Personalized Meal Plan")
    
    # Initialize meal planner
    planner = MealPlanner(df)
    
    # Generate meal plan
    meal_plan_result = planner.generate_meal_plan(
        target_calories=predicted_calories,
        target_protein=predicted_macros['protein'],
        target_carbs=predicted_macros['carbs'],
        target_fat=predicted_macros['fat'],
        target_fiber=25,
        meal_distribution={'breakfast': 0.25, 'lunch': 0.40, 'dinner': 0.35}
    )
    
    meal_plan = meal_plan_result['meal_plan']
    total_nutrition = meal_plan_result['total_nutrition']
    target_nutrition = meal_plan_result['target_nutrition']
    
    # Display meal plan
    col1, col2, col3 = st.columns(3)
    
    meals = {
        'breakfast': ('🌅 Breakfast', col1),
        'lunch': ('🍽️ Lunch', col2),
        'dinner': ('🌙 Dinner', col3)
    }
    
    for meal_name, (meal_title, col) in meals.items():
        with col:
            st.subheader(meal_title)
            if meal_plan[meal_name]:
                meal_cal = 0
                meal_prot = 0
                meal_carb = 0
                meal_fat = 0
                
                for food in meal_plan[meal_name]:
                    st.write(f"**{food['food_name']}**")
                    st.caption(f"Cal: {food['calories']:.0f} | P: {food['protein']:.1f}g | C: {food['carbohydrates']:.1f}g | F: {food['fat']:.1f}g")
                    meal_cal += food['calories']
                    meal_prot += food['protein']
                    meal_carb += food['carbohydrates']
                    meal_fat += food['fat']
                
                st.divider()
                st.metric("Total", f"{meal_cal:.0f} kcal")
                st.caption(f"P: {meal_prot:.1f}g | C: {meal_carb:.1f}g | F: {meal_fat:.1f}g")
            else:
                st.info("No foods selected")
    
    # Daily totals
    st.header("📈 Daily Totals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Target vs Actual")
        comparison_data = {
            'Nutrient': ['Calories', 'Protein', 'Carbs', 'Fat'],
            'Target': [
                target_nutrition['calories'],
                target_nutrition['protein'],
                target_nutrition['carbohydrates'],
                target_nutrition['fat']
            ],
            'Actual': [
                total_nutrition['calories'],
                total_nutrition['protein'],
                total_nutrition['carbohydrates'],
                total_nutrition['fat']
            ]
        }
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("Achievement Percentage")
        achievement = {
            'Nutrient': ['Calories', 'Protein', 'Carbs', 'Fat'],
            'Percentage': [
                (total_nutrition['calories'] / target_nutrition['calories'] * 100) if target_nutrition['calories'] > 0 else 0,
                (total_nutrition['protein'] / target_nutrition['protein'] * 100) if target_nutrition['protein'] > 0 else 0,
                (total_nutrition['carbohydrates'] / target_nutrition['carbohydrates'] * 100) if target_nutrition['carbohydrates'] > 0 else 0,
                (total_nutrition['fat'] / target_nutrition['fat'] * 100) if target_nutrition['fat'] > 0 else 0
            ]
        }
        achievement_df = pd.DataFrame(achievement)
        st.dataframe(achievement_df, use_container_width=True, hide_index=True)
        
        # Visualization
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.arange(len(achievement['Nutrient']))
        width = 0.6
        bars = ax.bar(x, achievement['Percentage'], width, color=['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3'])
        ax.set_ylabel('Percentage (%)')
        ax.set_title('Target Achievement')
        ax.set_xticks(x)
        ax.set_xticklabels(achievement['Nutrient'])
        ax.axhline(y=100, color='green', linestyle='--', alpha=0.5, label='100% Target')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # Algorithm Information
    with st.expander("ℹ️ About the Algorithms"):
        st.markdown("""
        ### Linear Regression
        - **Purpose**: Predicts daily calorie and macronutrient requirements
        - **Method**: Uses Mifflin-St Jeor equation with Linear Regression refinement
        - **Features**: Age, Gender, Height, Weight, Activity Level
        
        ### K-Nearest Neighbors (KNN)
        - **Purpose**: Finds nutritionally similar foods
        - **Method**: Euclidean distance metric on normalized nutritional features
        - **Output**: Top K most similar foods with similarity scores
        
        ### Greedy Algorithm
        - **Purpose**: Generates optimal daily meal plans
        - **Method**: Greedy selection minimizing nutritional gap at each step
        - **Output**: Balanced breakfast, lunch, and dinner plans
        """)
    
else:
    # Welcome screen
    st.info("👈 **Please fill in your profile information in the sidebar and click 'Generate Recommendations' to get started!**")
    
    # Show dataset info
    with st.expander("📊 Dataset Information"):
        st.write(f"**Total Foods in Dataset**: {len(df)}")
        st.write("**Available Nutrients**: Calories, Protein, Carbohydrates, Fat, Fiber")
        st.dataframe(df[['food_name', 'calories', 'protein', 'carbohydrates', 'fat']].head(20), use_container_width=True, hide_index=True)

