#  Customer Churn Analysis

##  Overview
This project analyzes customer churn behavior for a telecommunications company.  
The goal is to identify key factors influencing churn and build a predictive model that can help the business improve retention strategies.

---

##  Objectives
- Perform data cleaning and exploratory data analysis (EDA)
- Identify patterns and trends in customer churn
- Build and evaluate a logistic regression model to predict churn
- Interpret feature importance to support business decisions

---

##  Dataset
- **Source:** Telco Customer Churn dataset (public Kaggle dataset)
- **Rows:** ~7,000 customer records  
- **Features:** Demographics, subscription details, payment methods, and usage statistics  
- **Target:** `Churn` (Yes/No)

---

##  Analysis Summary
- Customers using **Fiber Optic internet** and **Paperless Billing** were more likely to churn.
- Customers with **partners** and longer **tenure** showed higher loyalty.
- Payment method and service type had significant predictive influence.

---

##  Model Summary
A **Logistic Regression** model was trained to classify customers as “likely to churn” or “retain.”

| Metric | Score |
|---------|--------|
| Accuracy | ~80% |
| Precision | ~78% |
| Recall | ~72% |

Key positive coefficients:
- `InternetService_Fiber optic`
- `PaperlessBilling_Yes`
- `PaymentMethod_Electronic check`

Key negative coefficients:
- `Partner_Yes`
- `tenure`

---

##  Technologies Used
- Python, Pandas, NumPy  
- Matplotlib, Seaborn  
- Scikit-learn (Logistic Regression, train/test split, metrics)

---

##  Key Insights
- Technical services and billing options strongly influence churn.  
- Demographic features have smaller but consistent effects.  
- Business actions: consider discounts or loyalty programs for fiber-optic users and electronic check payers.

---

## 🧑‍💻 Author
**Yanal Kat**  
Data Analyst / Business Information Systems  
