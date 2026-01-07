# EatWise – Personalized Nutrition & Meal Recommendation System

## Project Overview

EatWise is an AI-powered nutrition recommendation system designed as an academic coursework project. The system uses three fundamental AI/ML algorithms to provide personalized nutrition recommendations:

1. **Linear Regression** - Predicts daily calorie and macronutrient requirements
2. **K-Nearest Neighbors (KNN)** - Recommends nutritionally similar foods
3. **Greedy Algorithm** - Generates optimal daily meal plans

## Project Structure

```
EatWise/
│
├── app.py                           # Streamlit web application (MAIN UI)
├── data/
│   └── foods_nutrition.csv          # Nutrition dataset
│
├── src/
│   ├── __init__.py                  # Package initialization
│   ├── data_loader.py               # Data loading and preprocessing
│   ├── calorie_prediction.py       # Linear Regression for calorie prediction
│   ├── food_recommendation.py      # KNN for food recommendations
│   └── meal_planner.py             # Greedy algorithm for meal planning
│
├── notebooks/
│   └── EatWise_Main.ipynb          # Jupyter notebook version
│
├── requirements.txt                 # Python dependencies
├── run_ui.bat                       # Windows batch file to run app
├── run_ui.sh                        # Linux/Mac script to run app
├── HOW_TO_RUN.md                    # Detailed running instructions
└── README.md                        # Project documentation
```

## Features

- **Personalized Calorie Prediction**: Uses Linear Regression based on user profile (age, gender, height, weight, activity level)
- **Food Recommendations**: KNN algorithm finds nutritionally similar foods
- **Meal Planning**: Greedy algorithm generates balanced breakfast, lunch, and dinner plans
- **Visualizations**: Charts and graphs for better understanding of results

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure the dataset is in the `data/` folder:
   - The `foods_nutrition.csv` file should be present in the `data/` directory

## Usage

### 🚀 Running the Web Application (Recommended)

**Quick Start:**
```bash
streamlit run app.py
```

Or use the batch file (Windows):
```bash
run_ui.bat
```

The app will open automatically in your browser at `http://localhost:8501`

**Features:**
- Interactive web interface
- Real-time calculations
- Visual charts and graphs
- Easy-to-use sidebar for input
- Complete meal plan generation

See `HOW_TO_RUN.md` for detailed instructions.

### 📓 Running the Jupyter Notebook

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Navigate to `notebooks/EatWise_Main.ipynb`

3. Run all cells sequentially

### Customizing User Input

**In the Web App:**
- Use the sidebar to input your profile information
- Click "Generate Recommendations" to see results

**In the Notebook:**
Modify the user profile section:

```python
age = 25
gender = 'male'  # or 'female'
height_cm = 175
weight_kg = 70
activity_level = 'moderate'  # Options: 'sedentary', 'light', 'moderate', 'active', 'very_active'
goal = 'maintain'  # Options: 'maintain', 'lose', 'gain'
```

## Algorithms Explained

### 1. Linear Regression
- **Purpose**: Predict daily calorie and macronutrient requirements
- **Method**: Uses Mifflin-St Jeor equation as baseline with Linear Regression refinement
- **Features**: Age, Gender, Height, Weight, Activity Level
- **Output**: Daily calories, protein, carbohydrates, and fat targets

### 2. K-Nearest Neighbors (KNN)
- **Purpose**: Find nutritionally similar foods
- **Method**: Euclidean distance metric on normalized nutritional features
- **Features**: Calories, Protein, Carbohydrates, Fat, Fiber
- **Output**: Top K most similar foods with similarity scores

### 3. Greedy Algorithm
- **Purpose**: Generate optimal daily meal plans
- **Method**: Greedy selection that minimizes nutritional gap at each step
- **Strategy**: Weighted gap calculation prioritizing calories, then macros
- **Output**: Breakfast, lunch, and dinner plans with nutritional breakdown

## Dataset

The project uses a nutrition dataset containing:
- Food names
- Calories (Energy)
- Macronutrients: Protein, Carbohydrates, Fat
- Fiber content
- Additional micronutrients

## Requirements

- Python 3.7+
- Required packages listed in `requirements.txt`
- Streamlit (for web app)
- Jupyter Notebook (optional, for notebook version)

## Academic Justification

This project demonstrates:
- **Clean Code Structure**: Modular design with separate modules for each algorithm
- **Explainable AI**: Simple algorithms suitable for academic presentation
- **Reproducibility**: Well-documented code with clear explanations
- **Visualization**: Charts and graphs for result interpretation

## Limitations

- Meal plans may not perfectly match targets (greedy algorithm limitation)
- Does not account for user food preferences or dietary restrictions
- Could be enhanced with more sophisticated optimization algorithms

## Future Improvements

- Add user preference filtering
- Incorporate dietary restrictions (vegetarian, vegan, allergies)
- Use Genetic Algorithm for better meal plan optimization
- Add meal variety constraints
- Include micronutrient tracking

## Author

AI Coursework Project - EatWise

## License

This project is created for academic purposes.

