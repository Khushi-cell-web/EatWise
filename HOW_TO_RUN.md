# How to Run EatWise App in Cursor

## Step-by-Step Instructions

### Step 1: Open Terminal in Cursor
1. In Cursor, press `Ctrl + ~` (or `Ctrl + ` `) to open the integrated terminal
2. Or go to: **Terminal → New Terminal**

### Step 2: Verify You're in the Project Directory
```bash
# You should see the project files
dir
# or
ls
```

You should see:
- `app.py`
- `requirements.txt`
- `src/` folder
- `data/` folder

### Step 3: Install Dependencies (if not already installed)
```bash
pip install -r requirements.txt
```

This will install:
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- streamlit
- jupyter

### Step 4: Run the Streamlit App
```bash
streamlit run app.py
```

### Step 5: Access the App
After running the command, you'll see output like:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

1. **Cursor will automatically open the app in your browser**, OR
2. **Manually open**: Click the `http://localhost:8501` link, or copy-paste it into your browser

### Step 6: Use the App
1. **Fill in your profile** in the left sidebar:
   - Age
   - Gender (male/female)
   - Height (cm)
   - Weight (kg)
   - Activity Level
   - Goal (maintain/lose/gain)

2. **Click "🚀 Generate Recommendations"** button

3. **View your results**:
   - Daily nutritional requirements
   - Recommended foods
   - Personalized meal plan (breakfast, lunch, dinner)
   - Visualizations and charts

### Step 7: Stop the App
- Press `Ctrl + C` in the terminal to stop the Streamlit server

---

## Alternative: Using the Batch File (Windows)

Simply double-click `run_ui.bat` in the project folder, or run:
```bash
.\run_ui.bat
```

---

## Troubleshooting

### Issue: "streamlit: command not found"
**Solution**: Install streamlit
```bash
pip install streamlit
```

### Issue: "Module not found" errors
**Solution**: Install all requirements
```bash
pip install -r requirements.txt
```

### Issue: Port 8501 already in use
**Solution**: Use a different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: Can't find data file
**Solution**: Make sure `data/foods_nutrition.csv` exists
```bash
# Check if file exists
dir data
```

---

## Quick Start (All-in-One Command)

If you want to do everything at once:
```bash
pip install -r requirements.txt && streamlit run app.py
```

---

## Project Structure Reference

```
EatWise/
├── app.py                    ← Main Streamlit app (run this!)
├── requirements.txt          ← Dependencies
├── src/                      ← Python modules
│   ├── data_loader.py
│   ├── calorie_prediction.py
│   ├── food_recommendation.py
│   └── meal_planner.py
├── data/
│   └── foods_nutrition.csv   ← Dataset (required!)
└── notebooks/
    └── EatWise_Main.ipynb    ← Jupyter notebook version
```

---

## Tips

- **Keep the terminal open** while using the app
- **The app auto-reloads** when you save changes to `app.py`
- **Use the sidebar** to input your profile information
- **Check the terminal** for any error messages

---

## Need Help?

If you encounter any issues:
1. Check the terminal output for error messages
2. Verify all files are in the correct locations
3. Make sure Python and pip are installed correctly
4. Try reinstalling dependencies: `pip install -r requirements.txt --upgrade`

