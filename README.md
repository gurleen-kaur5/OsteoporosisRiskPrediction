# 🩺 Predictive Modeling of Osteoporosis Risk Using Advanced Ensemble Classifiers

## 📌 Project Overview
This research project develops and validates a highly accurate and clinically trustworthy Machine Learning (ML) model for the **proactive assessment of Osteoporosis risk**.  
Osteoporosis is a *“silent disease”* often detected too late, leading to severe fractures.  
Our primary goal was to build a **non-invasive, reliable screening tool** that emphasizes clinical safety by ensuring **zero false alarms**.

The final solution uses an optimized **CatBoost Classifier** deployed through a lightweight **Flask web application**, enabling healthcare providers or individuals to assess Osteoporosis risk using demographic, lifestyle, and clinical inputs.

---

## 🚀 Key Features and Achievements

### ✔️ Model Superiority  
Evaluated **eight Machine Learning classifiers**, with CatBoost outperforming all others.

### ✔️ Performance Ceiling  
Achieved a strong **Mean Cross-Validated AUC-ROC of `0.9231`**, showing excellent discriminatory power.

### ✔️ Novel Clinical Safety Focus  
Prioritized **Precision**, achieving  
**Perfect Precision = `1.0000`** on the test set.  
This ensures:
- Zero False Positives  
- Maximum clinical trust  
- No unnecessary diagnostic referrals  

### ✔️ Model Explainability (XAI)  
Used **SHAP analysis** to validate that predictions are heavily influenced by clinically meaningful factors:
- Age  
- Prior fractures  
- Hormonal changes  

### ✔️ Deployment  
Fully deployed using a **Flask backend**, with an accessible web interface for real-world usage.

---

## 🛠️ Methodology and Technical Stack

### 1. 📊 Data and Preprocessing  
Dataset: **1,958 patient records** containing demographic, lifestyle, and clinical variables.

#### 🔧 Key Preprocessing Steps:
- **Stratified Train-Test Split**  
  - 80% Training  
  - 20% Testing  
  - Maintains class balance  
- **CatBoost Categorical Handling**  
  - Model directly consumes raw categorical strings  
  - Avoids manual encoding  
  - Reduces bias and enhances stability  

---

### 2. ⚙️ Experimental Setup

| Component       | Technology           | Rationale |
|----------------|----------------------|-----------|
| **Primary Model** | CatBoost Classifier | Best handling of categorical data; high accuracy; robust |
| **Validation** | 5-Fold Cross-Validation | Ensures strong generalizability (`Mean AUC = 0.9231`) |
| **Programming** | Python (3.x) | Standard ML ecosystem |
| **Libraries** | pandas, numpy, scikit-learn, xgboost, catboost | Data processing + modeling |

---

### 3. 🌐 Deployment Stack

- **Backend:** Flask (Python) — hosts inference API  
- **Model Format:** Serialized CatBoost `.cbm` file  
- **Frontend:** HTML, CSS, JavaScript — user interface for entering inputs and showing predictions  



