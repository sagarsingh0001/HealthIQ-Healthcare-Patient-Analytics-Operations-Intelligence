# HealthIQ — Healthcare Patient Analytics Dashboard

> **Educational and analytical project. Not a clinical decision-making system.**

A portfolio-ready, end-to-end data analytics project built on a healthcare patient dataset covering 5,000 patient visits (January – July 2022). The project demonstrates the full data analyst workflow: data cleaning → SQL analysis → Python EDA → business insights → Power BI dashboard → Streamlit app → ML model.

---

## Business Problem

Healthcare operations teams need to understand:
- Which departments and visit types drive the most volume and cost
- How patient demographics relate to treatment patterns
- Which patients are at higher risk of readmission
- What the average recovery score looks like across departments

This project simulates that analytical workflow using a structured patient dataset.

---

## Dataset

| Column               | Description                                  | Type        |
|--------------------|----------------------------------------------|-------------|
| `patient_id`         | Unique patient identifier                    | Integer     |
| `visit_date`         | Date/time of hospital visit                 | Datetime    |
| `age_group`          | Patient age bracket (18-30, 31-45, 46-60, 60+) | Categorical |
| `gender`             | Patient gender (Male / Female)              | Categorical |
| `region`             | Geographic region (North, South, East, West) | Categorical |
| `department`         | Hospital department                          | Categorical |
| `treatment_type`     | Treatment administered                       | Categorical |
| `visit_type`         | Emergency or Routine                         | Categorical |
| `length_of_stay_days`| Days in hospital (0 – 11.9)                 | Numeric     |
| `treatment_cost`     | Cost in USD ($746 – $119,307)               | Numeric     |
| `recovery_score`     | Discharge recovery score (33 – 100)         | Numeric     |
| `readmission_risk`   | Risk category (Low / Medium / High)          | Categorical |

**Raw size:** 5,000 rows × 12 columns | **Date range:** Jan 2022 – Jul 2022

---

## Data Cleaning

Key steps performed in [`notebooks/01_data_cleaning.ipynb`](notebooks/01_data_cleaning.ipynb):

- No missing values or duplicates found
- `visit_date` converted from string to datetime
- All categorical columns verified for whitespace and inconsistent casing (none found)
- Numerical values validated (no negatives, no out-of-range values)
- `readmission_risk` binned from continuous probability (0.01–0.84) → Low / Medium / High
- 15–18 IQR outliers per numeric column retained (clinically plausible)
- Raw dataset preserved unchanged

See [`reports/data_cleaning_report.md`](reports/data_cleaning_report.md) for full details.

---

## Tools & Technologies

| Tool            | Purpose                            |
|----------------|------------------------------------|
| Python          | Data cleaning, EDA, ML             |
| Pandas / NumPy  | Data manipulation                  |
| Matplotlib / Seaborn | Static EDA visualisations    |
| Plotly          | Interactive Streamlit charts       |
| MySQL           | SQL analysis                       |
| Power BI        | Executive dashboard                |
| Streamlit       | Interactive analytics application  |
| Scikit-learn    | ML model (Random Forest)           |
| Joblib          | Model serialisation                |

---

## SQL Analysis

Five SQL scripts in the [`sql/`](sql/) folder answer 20+ analytical questions:

| File                          | Coverage                                      |
|------------------------------|-----------------------------------------------|
| `01_data_quality.sql`         | Null checks, range validation, distinct values |
| `02_basic_analysis.sql`       | Patient volume, demographics, visit trends     |
| `03_department_analysis.sql`  | LOS, recovery by department & treatment        |
| `04_cost_analysis.sql`        | Cost by dept, treatment, visit type; CTEs      |
| `05_risk_analysis.sql`        | Risk % by dept, age, visit type; window funcs  |

Load `cleaned_healthcare_data.csv` into MySQL as table `patient_data` to run the queries.

---

## Python EDA

Three Jupyter notebooks in [`notebooks/`](notebooks/):

| Notebook                         | Content                                 |
|---------------------------------|-----------------------------------------|
| `01_data_cleaning.ipynb`         | Full cleaning walkthrough               |
| `02_exploratory_analysis.ipynb`  | Demographics, operations, cost, risk    |
| `03_business_analysis.ipynb`     | Business questions answered with data   |

---

## Power BI Dashboard

Three-page dashboard specified in [`powerbi/HealthIQ_Dashboard_Spec.md`](powerbi/HealthIQ_Dashboard_Spec.md):

| Page                     | Content                                                    |
|-------------------------|------------------------------------------------------------|
| Executive Overview       | 7 KPI cards, monthly trend, dept chart, risk distribution  |
| Operations & Cost        | Cost by dept/treatment, LOS by dept, cost vs LOS scatter   |
| Patient Risk & Outcomes  | Risk by dept/age/visit type, recovery by dept, scatter     |

All pages include slicers for department, region, gender, age group, and visit type.

---

## Streamlit Application

Interactive analytics app in [`streamlit_app/`](streamlit_app/).

**Run:**

```bash
streamlit run streamlit_app/app.py
```

| Page               | Content                                               |
|-------------------|-------------------------------------------------------|
| Dashboard          | KPIs, monthly trend, department/risk charts           |
| Patient Analysis   | Demographics, data table, download                    |
| Cost & Operations  | Cost/LOS charts, department summary, download         |
| Risk Analysis      | Risk by dept/age/visit type, recovery vs risk, download |
| ML Prediction      | Enter patient details → predicted risk category       |

---

## Machine Learning

**Model:** Random Forest Classifier (class_weight='balanced')
**Target:** `readmission_risk` (Low / Medium / High)

| Metric           | Value  |
|-----------------|--------|
| CV F1 (weighted) | 0.465  |
| Test Accuracy    | 46.0%  |
| Weighted F1      | 0.477  |
| Weighted Precision | 0.496 |
| Weighted Recall  | 0.460  |

> The modest performance reflects near-zero correlations between features and the target in this dataset. The model serves as an educational demonstration of a classification pipeline with imbalanced classes.

See [`reports/ml_model_report.md`](reports/ml_model_report.md) for full details.

---

## Key Insights

1. **Balanced department volume:** All 5 departments handle 19–21% of visits (Orthopedics: 1,058, Cardiology: 995, General Medicine: 991, Pediatrics: 989, Neurology: 967).
2. **Routine visits dominate:** 68.6% routine vs 31.4% emergency.
3. **Total cost: $274.6M** across 5,000 visits. Average cost per visit: **$54,915**.
4. **Neurology & Cardiology** have the highest average treatment cost ($55,762 and $55,633 respectively).
5. **60% of patients are Low risk**; only 3.5% are High risk.
6. **60+ seniors** have the highest High-risk rate (4.5% vs 3.2% for mid-age groups).
7. **Near-zero correlations** between LOS, cost, and recovery — key clinical drivers (diagnosis codes, comorbidities) are absent from this dataset.

---

## Project Structure

```
healthiq-patient-analytics/
│
├── data/
│   ├── raw/                          # Original dataset (unchanged)
│   └── processed/                    # Cleaned dataset
│
├── sql/                              # 5 SQL analysis scripts
│
├── notebooks/                        # 3 Jupyter notebooks
│
├── models/                           # Trained ML pipeline (.pkl)
│
├── powerbi/                          # Dashboard specification
│
├── streamlit_app/                    # Interactive Streamlit app
│   ├── app.py
│   ├── data_loader.py
│   ├── analytics.py
│   ├── charts.py
│   ├── ml_predictor.py
│   ├── requirements.txt
│   └── README.md
│
├── reports/
│   ├── data_dictionary.md
│   ├── data_cleaning_report.md
│   ├── business_insights.md
│   └── ml_model_report.md
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Installation

```bash
# Clone or download the repository
cd healthiq-patient-analytics

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app/app.py
```

For Jupyter notebooks:

```bash
pip install jupyter
jupyter notebook notebooks/
```

---

## Running Streamlit

```bash
streamlit run streamlit_app/app.py
```

The app opens at `http://localhost:8501`.

---

## Limitations

1. Dataset appears to be synthetically generated — near-zero correlations between numeric features limit ML performance.
2. No diagnosis codes or ICD fields — the strongest real-world predictor of cost and readmission is absent.
3. One visit per patient — no longitudinal patient history available.
4. 7-month window — seasonal patterns cannot be fully assessed.
5. `readmission_risk` is a binned probability score of unknown origin and should not be interpreted as a clinically validated label.

---

## Disclaimer

This project is **for educational and portfolio purposes only**. It is not a clinical decision-making system, does not provide medical advice, and should not be used in real healthcare settings without proper clinical validation.
