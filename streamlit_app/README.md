# HealthIQ Streamlit App

Interactive analytics frontend for the **HealthIQ — Healthcare Patient Analytics** project.

---

## Purpose

This application provides an interactive interface to explore the healthcare patient dataset. It covers patient demographics, hospital operations, treatment costs, readmission risk, and an optional ML-based risk predictor.

---

## Installation

```bash
# From the project root
pip install -r streamlit_app/requirements.txt
```

Or from within the `streamlit_app/` folder:

```bash
pip install -r requirements.txt
```

---

## Data Setup

The app reads the cleaned dataset from:

```
data/processed/cleaned_healthcare_data.csv
```

Run the data cleaning notebook first if the file does not exist:

```bash
jupyter notebook notebooks/01_data_cleaning.ipynb
```

---

## How to Run

From the **project root** (`healthiq-patient-analytics/`):

```bash
streamlit run streamlit_app/app.py
```

The app will open at `http://localhost:8501`.

---

## Application Pages

### Dashboard
- KPI cards: Total Patients, Total Visits, Total Cost, Avg Cost, Avg LOS, Avg Recovery, High Risk %
- Monthly visit trend
- Department distribution
- Visit type distribution
- Readmission risk distribution
- Download filtered dataset as CSV

### Patient Analysis
- Age group, gender, region, department, visit type charts
- Interactive data table with download

### Cost & Operations
- Average cost by department and treatment type
- Average LOS by department
- Average cost by visit type
- Cost vs LOS scatter chart
- Department summary table with download

### Risk Analysis
- High/Medium/Low risk distribution
- Risk by department (stacked bar)
- Risk by age group
- Risk by visit type
- Recovery score vs risk (boxplot)
- Filtered risk table with download

### ML Prediction *(if model is available)*
- Enter patient details (age group, gender, department, treatment type, LOS, cost, recovery score)
- Click **Predict Risk** to get a model-predicted risk category
- Displays predicted probabilities (High / Medium / Low)

---

## ML Model Notes

- **Model:** Random Forest classifier (class_weight='balanced')
- **Target:** readmission_risk (Low / Medium / High)
- **Test accuracy:** ~46%
- **Weighted F1:** ~0.48

The model's modest performance reflects the low correlations between features and the risk label in this dataset. Results are for educational purposes only.

---

## Sidebar Filters

All pages respond to sidebar filters:
- Date range
- Department
- Region
- Gender
- Age Group
- Visit Type

Leave filters empty to show all data.

---

## Disclaimer

> This application is for **educational and analytical purposes only**. It is not a clinical decision-making system and does not provide medical advice or diagnoses.
