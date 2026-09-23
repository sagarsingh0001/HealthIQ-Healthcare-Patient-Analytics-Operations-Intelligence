# Business Insights — HealthIQ Patient Analytics

**Dataset:** 5,000 patient visits | January 2022 – July 2022
**All numbers are derived from the actual cleaned dataset.**

---

## 1. Patient Insights

### 1.1 The dataset covers 5,000 unique patient visits over 7 months
- Every `patient_id` appears exactly once, confirming one visit per patient.
- The visit volume is fairly consistent month-to-month, ranging from **656 visits (July)** to **744 visits (Jan, Mar, May)**, with a slight dip in July likely due to partial month data.

### 1.2 The 31–45 age group is the largest patient segment
- **31–45 years:** 1,716 patients (34.3%)
- **18–30 years:** 1,283 patients (25.7%)
- **46–60 years:** 1,271 patients (25.4%)
- **60+ years:** 730 patients (14.6%)

Working-age adults (18–45) account for **60%** of all visits, suggesting the dataset skews toward younger adults.

### 1.3 Gender distribution is near-equal
- Male: 2,508 (50.2%)
- Female: 2,492 (49.8%)

No significant gender imbalance exists in this dataset.

### 1.4 Regional distribution is balanced
- West: 1,290 (25.8%)
- North: 1,282 (25.6%)
- East: 1,217 (24.3%)
- South: 1,211 (24.2%)

No single region disproportionately dominates patient volume.

---

## 2. Operational Insights

### 2.1 Orthopedics is the highest-volume department
| Department       | Visits | % of Total |
|-----------------|--------|-----------|
| Orthopedics      | 1,058  | 21.2%     |
| Cardiology       | 995    | 19.9%     |
| General Medicine | 991    | 19.8%     |
| Pediatrics       | 989    | 19.8%     |
| Neurology        | 967    | 19.3%     |

Volume is **highly balanced** across all 5 departments — each handling roughly 19–21% of visits. No single department is overwhelmed relative to others.

### 2.2 Routine visits account for 69% of all visits
- Routine: 3,432 (68.6%)
- Emergency: 1,568 (31.4%)

This is a reasonably healthy ratio, suggesting planned care is more common than unplanned emergency visits.

### 2.3 Emergency visits have a slightly longer average length of stay
- Emergency visits avg LOS: **4.10 days**
- Routine visits avg LOS: **4.04 days**

The difference is small (0.06 days), indicating that LOS is not strongly driven by visit urgency in this dataset.

### 2.4 Pediatrics has the longest average length of stay
| Department       | Avg LOS (days) |
|-----------------|---------------|
| Pediatrics       | 4.14           |
| General Medicine | 4.07           |
| Neurology        | 4.06           |
| Cardiology       | 4.03           |
| Orthopedics      | 4.01           |

Differences across departments are minimal (range: 4.01–4.14 days), suggesting LOS is relatively uniform across the hospital.

### 2.5 Correlations between LOS, cost, and recovery are near-zero
- LOS ↔ Treatment Cost: **r = -0.022**
- LOS ↔ Recovery Score: **r = +0.012**
- Treatment Cost ↔ Recovery Score: **r = -0.015**

These near-zero correlations indicate that in this dataset, longer stays do not translate into higher costs or better recovery outcomes — and higher-cost treatments do not predict better recovery. This is an important dataset limitation to acknowledge.

---

## 3. Financial Insights

### 3.1 Total treatment cost across all visits is $274,577,359
- Average cost per visit: **$54,915**
- Median cost: **$55,124**
- Range: $746 – $119,307

The distribution is roughly symmetric, with mean and median nearly equal, indicating cost is not heavily skewed by a small number of extreme cases.

### 3.2 Neurology and Cardiology are the most expensive departments on average
| Department       | Avg Cost  |
|-----------------|-----------|
| Neurology        | $55,762   |
| Cardiology       | $55,633   |
| Orthopedics      | $54,913   |
| Pediatrics       | $54,782   |
| General Medicine | $53,506   |

Differences are modest (~$2,200 spread), meaning no single department dramatically exceeds others in average cost.

### 3.3 Surgery is the most expensive treatment type
| Treatment Type | Avg Cost  |
|---------------|-----------|
| Surgery        | $55,327   |
| Medication     | $55,112   |
| Observation    | $54,958   |
| Therapy        | $54,252   |

The cost spread across treatment types is narrow (~$1,100). Surgery being most expensive is expected but the gap is smaller than might be assumed.

### 3.4 Routine visits average slightly higher cost than Emergency visits
- Routine: $55,012
- Emergency: $54,705

The difference (~$307) is negligible, suggesting visit type does not significantly drive treatment cost.

### 3.5 Younger patients (18–30) have the highest average treatment cost
- 18–30: $55,871
- 31–45: $54,748
- 46–60: $54,749
- 60+: $53,920

The 60+ group has the lowest average cost, which may reflect shorter or less interventional visits for elderly patients in this dataset.

---

## 4. Risk Insights

### 4.1 The majority of patients are classified as Low risk
- Low (0.00–0.30): **3,002 patients (60.0%)**
- Medium (0.30–0.60): **1,822 patients (36.4%)**
- High (0.60–1.00): **176 patients (3.5%)**

High-risk patients represent a small but operationally significant segment — they are likely to require the most post-discharge support.

### 4.2 Orthopedics has the highest proportion of High-risk patients
| Department       | High Risk % |
|-----------------|------------|
| Orthopedics      | 3.78%       |
| Pediatrics       | 3.74%       |
| General Medicine | 3.53%       |
| Cardiology       | 3.42%       |
| Neurology        | 3.10%       |

Differences across departments are small (range: 3.10–3.78%), indicating no department has a dramatically elevated risk profile.

### 4.3 Emergency visits have a higher High-risk rate than Routine visits
- Emergency: High risk = 61/1,568 = **3.9%**
- Routine: High risk = 115/3,432 = **3.4%**

Emergency patients are modestly more likely to be High-risk, which aligns with the expectation that unplanned visits are associated with more severe conditions.

### 4.4 The 60+ age group has the highest High-risk rate
| Age Group | High Risk % |
|----------|------------|
| 18-30     | 3.7%        |
| 31-45     | 3.2%        |
| 46-60     | 3.2%        |
| 60+       | 4.5%        |

Senior patients (60+) have a noticeably higher High-risk rate (4.5% vs 3.2% for mid-age groups), consistent with greater clinical complexity in older patients.

### 4.5 Recovery scores are similar across risk categories
| Risk Category | Avg Recovery Score |
|--------------|-------------------|
| High          | 73.81              |
| Medium        | 74.82              |
| Low           | 74.71              |

Recovery score does not clearly separate risk categories in this dataset. This suggests that the readmission risk score (originally a continuous probability) is not strongly correlated with in-hospital recovery outcomes alone.

---

## Key Takeaways

1. **Volume is balanced**: All departments handle comparable patient volumes (19–21% each).
2. **Costs are uniform**: Average treatment costs are similar across departments and treatment types ($53K–$56K range).
3. **Risk is low overall**: 60% of patients are Low risk; only 3.5% are High risk.
4. **60+ patients warrant attention**: Senior patients have the highest readmission risk (4.5%) and the lowest average treatment cost — monitoring post-discharge outcomes for this group is important.
5. **Weak correlations**: LOS, cost, and recovery score are not strongly correlated with each other, suggesting they are independently influenced by factors not captured in this dataset (e.g., diagnosis severity, comorbidities).
6. **Emergency visits**: Slightly higher risk and LOS than Routine, but differences are modest.

---

## Limitations

- This dataset does not include diagnosis or diagnosis codes, which are typically the strongest predictors of cost, LOS, and readmission.
- The original readmission risk column is a pre-computed probability score of unknown origin. Its interpretation should be treated with caution.
- With near-zero correlations between key numerics, this dataset may be partially synthetic or generated with limited cross-variable relationships.
- One visit per patient means longitudinal patient patterns (repeat visits, chronic conditions) cannot be analyzed.
