# Data Cleaning Report — HealthIQ Patient Analytics

**Dataset:** `healthcare_patient_analytics_seaborn.csv`
**Cleaned Output:** `data/processed/cleaned_healthcare_data.csv`
**Cleaned by:** `notebooks/01_data_cleaning.ipynb`

---

## Summary Table

| Issue                          | Count | Action                                      |
|-------------------------------|------:|---------------------------------------------|
| Missing values                |     0 | None — dataset is complete                  |
| Duplicate rows                |     0 | None found                                  |
| Negative `length_of_stay_days`|     0 | None found                                  |
| Negative `treatment_cost`     |     0 | None found                                  |
| Negative `recovery_score`     |     0 | None found                                  |
| Whitespace in categories      |     0 | None found                                  |
| Inconsistent capitalisation   |     0 | None found                                  |
| IQR outliers — LOS            |    15 | Retained (see Outliers section)             |
| IQR outliers — cost           |    15 | Retained (see Outliers section)             |
| IQR outliers — recovery_score |    18 | Retained (see Outliers section)             |
| `visit_date` format           | 5,000 | Converted from string to datetime           |
| `readmission_risk` encoding   | 5,000 | Converted from 0–1 float → Low/Medium/High  |

---

## Original Dataset

| Metric          | Value          |
|----------------|----------------|
| Rows            | 5,000          |
| Columns         | 12             |
| Date range      | 2022-01-01 → 2022-07-28 |
| Unique patients | 5,000          |

## Final Dataset

| Metric          | Value  |
|----------------|--------|
| Rows            | 5,000  |
| Columns         | 12     |
| Rows removed    | 0      |

---

## Detailed Findings

### 1. Missing Values
No missing values were found in any column. No imputation was required.

### 2. Duplicate Rows
No duplicate rows were found. All 5,000 rows were retained.

### 3. Data Types
- `visit_date` was stored as a string (`object`). It was converted to `datetime64` to enable time-series analysis.
- All other columns had appropriate types on load.

### 4. Categorical Standardisation
All categorical columns (`age_group`, `gender`, `region`, `department`, `treatment_type`, `visit_type`) were inspected for:
- Leading/trailing whitespace → None found
- Inconsistent capitalisation → None found
- Unexpected values → None found

Categories discovered:

| Column          | Values                                           |
|----------------|--------------------------------------------------|
| age_group       | 18-30, 31-45, 46-60, 60+                         |
| gender          | Female, Male                                     |
| region          | East, North, South, West                         |
| department      | Cardiology, General Medicine, Neurology, Orthopedics, Pediatrics |
| treatment_type  | Medication, Observation, Surgery, Therapy        |
| visit_type      | Emergency, Routine                               |

### 5. Numerical Validation

| Column                | Min   | Max        | Valid? |
|----------------------|-------|------------|--------|
| length_of_stay_days  | 0.0   | 11.9       | Yes    |
| treatment_cost       | 746   | 119,307    | Yes    |
| recovery_score       | 33    | 100        | Yes    |
| readmission_risk     | 0.01  | 0.84       | Yes    |

No negative values were found. All values fall within clinically plausible ranges.

### 6. Outliers

IQR-based outlier analysis was performed on numeric columns. Outliers were **retained** for the following reasons:
- `length_of_stay_days` outliers (15 rows, values 9.5–11.9 days) are clinically valid; some patients do require extended care.
- `treatment_cost` outliers (15 rows, values above $108,163) can occur for complex procedures such as surgery combined with extended stays.
- `recovery_score` outliers (18 rows, values below 43) represent patients with genuinely poor recovery outcomes and should not be removed.

Removing these records would discard real variation and bias the analysis.

### 7. `readmission_risk` Encoding

The original column stores a continuous probability score (0.01–0.84). For analysis and ML classification, this was binned into three categories:

| Category | Range       | Count |
|---------|-------------|-------|
| Low     | 0.00 – 0.30 | 3,002 |
| Medium  | 0.30 – 0.60 | 1,822 |
| High    | 0.60 – 1.00 |   176 |

This encoding is applied in the cleaned dataset. The original raw file is unchanged.

---

## Assumptions

1. Each row represents one visit by one patient. The `patient_id` is unique per row, meaning this dataset records one visit per patient (not multiple visits for the same patient over time).
2. The `readmission_risk` column is interpreted as a continuous probability score from an external source and binned using standard thresholds (Low <0.30, Medium 0.30–0.60, High ≥0.60).
3. Outliers are retained because they are clinically plausible.
4. The dataset covers a 7-month period (January 2022 – July 2022).
