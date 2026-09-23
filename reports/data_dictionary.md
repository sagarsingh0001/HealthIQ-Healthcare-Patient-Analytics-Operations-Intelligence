# Data Dictionary — HealthIQ Patient Analytics

## What Does One Row Represent?

Each row represents **a single hospital visit by a single patient**. In this dataset, every `patient_id` appears exactly once, so each row is both a unique patient and a unique visit.

---

## Column Definitions

| Column               | Description                                                                 | Data Type   | Example           |
|---------------------|-----------------------------------------------------------------------------|-------------|-------------------|
| `patient_id`         | Unique numeric identifier for each patient/visit                            | Integer     | 1, 42, 5000       |
| `visit_date`         | Date and time of the hospital visit                                          | Datetime    | 2022-03-15 08:00  |
| `age_group`          | Patient age bracket at time of visit                                         | Categorical | 18-30, 31-45, 46-60, 60+ |
| `gender`             | Patient gender                                                               | Categorical | Male, Female      |
| `region`             | Geographic region where the patient is registered                            | Categorical | North, South, East, West |
| `department`         | Hospital department that handled the visit                                   | Categorical | Cardiology, General Medicine, Neurology, Orthopedics, Pediatrics |
| `treatment_type`     | Type of treatment administered during the visit                              | Categorical | Medication, Observation, Surgery, Therapy |
| `visit_type`         | Classification of the visit                                                  | Categorical | Emergency, Routine |
| `length_of_stay_days`| Number of days the patient stayed in hospital (fractional days allowed)      | Numeric (float) | 0.0 – 11.9    |
| `treatment_cost`     | Total cost of treatment in USD                                               | Numeric (float) | 746 – 119,307  |
| `recovery_score`     | Score representing patient recovery status at discharge (higher = better)   | Numeric (float) | 33 – 100       |
| `readmission_risk`   | Risk of patient readmission. In raw data: continuous probability 0.01–0.84. In cleaned data: binned to Low / Medium / High | Float → Categorical | Low, Medium, High |

---

## Categorical Value Reference

### `age_group`
| Value | Meaning         |
|-------|----------------|
| 18-30 | Young adults    |
| 31-45 | Middle-aged     |
| 46-60 | Older adults    |
| 60+   | Seniors         |

### `gender`
| Value  | Meaning |
|--------|---------|
| Male   | Male    |
| Female | Female  |

### `region`
| Value | Meaning      |
|-------|-------------|
| North | North region |
| South | South region |
| East  | East region  |
| West  | West region  |

### `department`
| Value            | Meaning                                          |
|-----------------|--------------------------------------------------|
| Cardiology       | Heart and cardiovascular conditions              |
| General Medicine | General and non-specialist care                 |
| Neurology        | Brain, spine, and nervous system conditions     |
| Orthopedics      | Bone, joint, and musculoskeletal conditions     |
| Pediatrics       | Care for children and young patients            |

### `treatment_type`
| Value       | Meaning                               |
|------------|---------------------------------------|
| Medication  | Drug-based treatment                  |
| Observation | Monitoring without active treatment   |
| Surgery     | Surgical procedure                    |
| Therapy     | Physical, occupational, or other therapy |

### `visit_type`
| Value     | Meaning                      |
|----------|------------------------------|
| Emergency | Unplanned emergency visit    |
| Routine   | Scheduled/planned visit      |

### `readmission_risk` (cleaned dataset)
| Value  | Raw Probability Range | Meaning                            |
|--------|----------------------|------------------------------------|
| Low    | 0.00 – 0.30          | Low likelihood of readmission      |
| Medium | 0.30 – 0.60          | Moderate likelihood of readmission |
| High   | 0.60 – 1.00          | High likelihood of readmission     |

---

## Numeric Ranges (from cleaned dataset)

| Column               | Min   | Max       | Mean     | Median   |
|---------------------|-------|-----------|----------|----------|
| length_of_stay_days | 0.0   | 11.9      | 4.06     | 4.0      |
| treatment_cost      | 746   | 119,307   | 54,915   | 55,124   |
| recovery_score      | 33    | 100       | 74.7     | 75.0     |
