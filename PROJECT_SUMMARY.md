# EatWise Project - Quick Reference

## 🎯 What This Project Does

EatWise is an AI-powered nutrition recommendation system that:
1. **Predicts** your daily calorie and macronutrient needs (Linear Regression)
2. **Recommends** nutritionally similar foods (KNN Algorithm)
3. **Generates** personalized meal plans (Greedy Algorithm)

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | **Main web application** - Run this for the UI |
| `requirements.txt` | Python dependencies |
| `run_ui.bat` | Quick launcher for Windows |
| `HOW_TO_RUN.md` | Detailed running instructions |
| `README.md` | Complete project documentation |

## 🚀 Quick Start

```bash
# 1. Install dependencies (first time only)
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

## 📂 Project Structure

```
EatWise/
├── app.py              ← Web UI (Streamlit)
├── src/                ← Core algorithms
│   ├── data_loader.py
│   ├── calorie_prediction.py
│   ├── food_recommendation.py
│   └── meal_planner.py
├── data/               ← Dataset
│   └── foods_nutrition.csv
└── notebooks/         ← Jupyter notebook version
    └── EatWise_Main.ipynb
```

## 🔧 Technologies Used

- **Python 3.7+**
- **Streamlit** - Web UI framework
- **scikit-learn** - ML algorithms (Linear Regression, KNN)
- **pandas** - Data processing
- **matplotlib/seaborn** - Visualizations

## 📝 Algorithms

1. **Linear Regression** → Calorie prediction
2. **K-Nearest Neighbors** → Food recommendations
3. **Greedy Algorithm** → Meal planning

## 🎓 Academic Use

Perfect for:
- AI/ML coursework projects
- Algorithm demonstration
- Nutrition science projects
- Data science portfolios

---

**Need help?** Check `HOW_TO_RUN.md` for detailed instructions.

