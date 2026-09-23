# ML Model Report — HealthIQ Readmission Risk Predictor

**Model File:** `models/readmission_risk_pipeline.pkl`
**Target:** `readmission_risk` (Low / Medium / High)
**Date:** 2024

---

## 1. Problem Statement

Predict whether a patient will be classified as **Low**, **Medium**, or **High** readmission risk based on their demographics, visit details, and clinical metrics.

This is a **multi-class classification** problem.

---

## 2. Dataset

- **Rows used:** 5,000
- **Train/Test split:** 80% / 20% (4,000 train, 1,000 test), stratified by target
- **Date range:** January 2022 – July 2022

---

## 3. Target Variable

| Class  | Count | % of Total |
|--------|------:|-----------|
| Low    | 3,002 | 60.0%     |
| Medium | 1,822 | 36.4%     |
| High   |   176 |  3.5%     |

The dataset has **significant class imbalance**: Low risk is the majority class (60%). Without correction, all models default to predicting "Low" for every row.

**Data Leakage Check:** The original `readmission_risk` column was a continuous probability score (0.01–0.84) that was binned to create the target. No feature in the dataset is directly derived from this value. No data leakage was detected.

---

## 4. Features Used

| Feature              | Type        | Notes                                     |
|--------------------|-------------|-------------------------------------------|
| age_group           | Categorical | Encoded with OrdinalEncoder               |
| gender              | Categorical | Encoded with OrdinalEncoder               |
| region              | Categorical | Encoded with OrdinalEncoder               |
| department          | Categorical | Encoded with OrdinalEncoder               |
| treatment_type      | Categorical | Encoded with OrdinalEncoder               |
| visit_type          | Categorical | Encoded with OrdinalEncoder               |
| length_of_stay_days | Numeric     | Scaled with StandardScaler                |
| treatment_cost      | Numeric     | Scaled with StandardScaler                |
| recovery_score      | Numeric     | Scaled with StandardScaler                |

---

## 5. Preprocessing

A **scikit-learn Pipeline** was used to chain preprocessing and the model:

```
ColumnTransformer
  ├── OrdinalEncoder → categorical features
  └── StandardScaler → numeric features
        ↓
    Classifier
```

`class_weight='balanced'` was applied to all models to address class imbalance.

---

## 6. Models Evaluated

All models used `class_weight='balanced'` and 5-fold stratified cross-validation.

| Model               | CV F1 (weighted) | Test Accuracy | Weighted F1 | Precision | Recall |
|--------------------|-----------------|--------------|------------|----------|--------|
| Logistic Regression | 0.346 ± 0.011   | 0.291         | 0.350       | 0.481    | 0.291  |
| Decision Tree       | 0.371 ± 0.041   | 0.407         | 0.442       | 0.501    | 0.407  |
| **Random Forest**   | **0.465 ± 0.011**| **0.460**    | **0.477**  | **0.496**| **0.460** |

---

## 7. Selected Model: Random Forest

**Reason for selection:** Random Forest achieved the highest CV F1 and test accuracy, with the most consistent cross-validation score (lowest standard deviation among the balanced models).

### Per-Class Metrics (Test Set)

| Class  | Precision | Recall | F1-score | Support |
|--------|----------|--------|---------|---------|
| Low    | 0.60      | 0.54   | 0.57    | 600     |
| Medium | 0.37      | 0.36   | 0.36    | 365     |
| High   | 0.03      | 0.09   | 0.04    | 35      |

### Confusion Matrix (Low / Medium / High)

```
           Pred Low  Pred Medium  Pred High
True Low      325        217         58
True Medium   194        132         39
True High      20         12          3
```

---

## 8. Key Limitations

1. **Near-zero correlations:** The three numeric features (`length_of_stay_days`, `treatment_cost`, `recovery_score`) have correlations with each other and with the target close to zero (|r| < 0.025). The features simply do not predict the target well.

2. **Class imbalance:** Only 3.5% of patients are High risk. Even with balanced weights, the model rarely correctly predicts High risk (recall of only 9%).

3. **Synthetic data characteristics:** The uniformly random correlations suggest the dataset may have been synthetically generated with limited cross-variable relationships.

4. **No diagnosis codes:** In real clinical settings, ICD codes or diagnosis fields are the strongest predictors of readmission. Their absence severely limits model performance.

5. **One visit per patient:** Without longitudinal patient history (prior admissions, comorbidities), the predictive signal available is minimal.

---

## 9. What This Model Can and Cannot Do

| Can Do                                          | Cannot Do                             |
|------------------------------------------------|---------------------------------------|
| Return a probability estimate for risk classes  | Accurately identify High-risk patients|
| Serve as a demo of a clinical ML pipeline       | Replace clinical judgment             |
| Illustrate how imbalanced data affects models   | Be deployed in a real healthcare setting|

---

## 10. Deployment

The complete preprocessing + model pipeline is saved as a single pickle file:

```python
import joblib
pipeline = joblib.load('models/readmission_risk_pipeline.pkl')
prediction = pipeline.predict(X_new)
probabilities = pipeline.predict_proba(X_new)
```

---

## 11. Disclaimer

> This model is built for **educational and portfolio purposes** only. It is not validated for clinical use and must not be used to make actual medical decisions.
