# Project 5: Predictive Maintenance (Machine Failure Prediction)

## Overview
This project explores **predictive maintenance** using the publicly available **AI4I 2020 dataset**  
(S. Matzka, *Explainable Artificial Intelligence for Predictive Maintenance Applications*, AI4I 2020).

The goal is to predict **whether a machine will fail**, based on sensor and operational readings such as  
air temperature, process temperature, rotational speed, torque, and tool wear.

---

## Objectives
- Analyze sensor data and identify patterns linked to equipment failure.  
- Build and evaluate machine-learning models for predictive maintenance.  
- Compare baseline (Random Forest) and advanced (XGBoost) models.  
- Interpret the most influential failure indicators.

---

## Workflow

### 1. Data Exploration & Cleaning
- Checked types, missing values, and distributions.  
- Dropped irrelevant identifiers (`UDI`).  
- Encoded categorical columns (`Product ID`, `Type`).

### 2. Feature Analysis
- Examined correlations among numeric features.  
- Compared average operational metrics between failure / non-failure cases.  
- Visualized target balance and numeric distributions.

### 3. Modeling & Evaluation
- Split data: 80 % training, 20 % validation.  
- **Random Forest Classifier** as baseline: 99.9 % accuracy, F1 ≈ 0.985.  
- **XGBoost Classifier** achieved identical performance, confirming model robustness.

### 4. Feature Importance
- Key predictors: **Overstrain Failure (OSF)**, **Power Failure (PWF)**,  
  **Heat Dissipation Failure (HDF)**, **Tool Wear Failure (TWF)**.  
- Operational factors (rotational speed, torque) contribute secondary predictive power.

---

## Results

| Metric | Random Forest | XGBoost |
|:--------|:-------------:|:--------:|
| **Accuracy** | 0.9990 | 0.9990 |
| **Precision** | 1.0000 | 1.0000 |
| **Recall** | 0.9706 | 0.9706 |
| **F1 Score** | 0.9851 | 0.9851 |

- Both models show near-perfect classification on validation data.  
- Very few false negatives → strong recall for failure detection.  
- Balanced performance ensures reliability in production settings.

---

## Conclusion
Predictive maintenance models can accurately identify potential machine failures before they occur.  
This project demonstrates how sensor data and machine-learning techniques can be combined to improve reliability, reduce downtime, and optimize maintenance schedules.

---

## Tech Stack
`Python`, `pandas`, `NumPy`, `scikit-learn`, `XGBoost`, `Matplotlib`, `Seaborn`, `Jupyter`

---

## Next Steps could be
- Extend to **real-time prediction pipelines** using streaming data (e.g., Kafka, AWS IoT).  
- Implement **explainability** methods like SHAP for detailed model insights.  
- Evaluate **anomaly-detection** or **time-series** approaches for continuous monitoring.


