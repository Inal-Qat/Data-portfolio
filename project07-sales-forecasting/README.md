# Retail Sales Forecasting with Machine Learning

**Goal:** Build and evaluate machine learning models to predict daily product sales across multiple stores and product families.  
This project explores data preprocessing, feature engineering, and model evaluation using **Random Forest** and **XGBoost** regressors.

---

## Project Overview

Accurate sales forecasting helps retail businesses manage inventory, reduce waste, and optimize promotions.  
Using real-world transactional data, this project predicts daily sales values and identifies the most important drivers of demand.

**Main objectives:**
- Clean and merge large, multi-table sales datasets  
- Engineer date-based and promotional features  
- Train and evaluate baseline models  
- Interpret model results through feature importance and error analysis  

---

## Tech Stack

- **Python**  
- **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**  
- **Scikit-learn** for baseline models  
- **XGBoost** for advanced regression  
- **Jupyter Notebook** for development  

---

## Model Performance

| Model | RMSE | Notes |
|:------|------:|:------|
| Random Forest Regressor | **318.05** | Strong baseline with balanced accuracy |
| XGBoost Regressor | **348.92** | Slightly higher error but more interpretable |

**Key features driving sales predictions:**
- `family` (product type/category)  
- `onpromotion` (promotion activity)  
- `type_x` (store type)  
- Temporal features (`year`, `month`, `day_of_week`)

---

## Results and Insights

- The **Random Forest** model provided the best baseline RMSE.  
- The **XGBoost** model allowed a deeper look into **feature importance**.  
- Clear seasonality and promotional patterns influence daily sales.  
- Feature importance and scatter plots show a good model fit, with limited noise.

---

## Next Steps

- Apply **hyperparameter tuning** for XGBoost  
- Engineer **lag features** for temporal context  
- Integrate **store-level metadata** (e.g., location, cluster)  
- Extend evaluation with **cross-validation and time-series splits**

---

## Learning Outcomes

This project demonstrates:
- Proficiency with **data cleaning and feature engineering**
- Model comparison using regression metrics (RMSE)
- Visualization and interpretability of ML models

