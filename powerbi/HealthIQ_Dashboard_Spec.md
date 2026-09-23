# Power BI Dashboard Specification — HealthIQ

> **Note:** Power BI `.pbix` files cannot be auto-generated programmatically. This document provides the complete specification to build the dashboard manually in Power BI Desktop.
>
> **Data Source:** `data/processed/cleaned_healthcare_data.csv` → load as table named `patient_data`

---

## Data Source Setup

1. Open Power BI Desktop
2. **Get Data → Text/CSV** → select `cleaned_healthcare_data.csv`
3. In Power Query:
   - Set `visit_date` → Data Type: **Date/Time**
   - Set `length_of_stay_days`, `treatment_cost`, `recovery_score` → **Decimal Number**
   - Set all categorical columns → **Text**
4. Rename the table: `patient_data`
5. Close & Apply

---

## DAX Measures

Create the following measures in a dedicated **Measures** table or in `patient_data`:

```dax
Total Patients =
DISTINCTCOUNT(patient_data[patient_id])

Total Visits =
COUNTROWS(patient_data)

Total Treatment Cost =
SUM(patient_data[treatment_cost])

Average Treatment Cost =
AVERAGE(patient_data[treatment_cost])

Average Length of Stay =
AVERAGE(patient_data[length_of_stay_days])

Average Recovery Score =
AVERAGE(patient_data[recovery_score])

High Risk Count =
CALCULATE(COUNTROWS(patient_data), patient_data[readmission_risk] = "High")

High Risk % =
DIVIDE([High Risk Count], [Total Visits], 0) * 100

Medium Risk % =
DIVIDE(
    CALCULATE(COUNTROWS(patient_data), patient_data[readmission_risk] = "Medium"),
    [Total Visits], 0
) * 100

Low Risk % =
DIVIDE(
    CALCULATE(COUNTROWS(patient_data), patient_data[readmission_risk] = "Low"),
    [Total Visits], 0
) * 100

Monthly Visits =
COUNTROWS(patient_data)
```

---

## PAGE 1 — Executive Overview

### Layout
- Background: White (#FFFFFF)
- Title: **HealthIQ — Executive Overview** (top centre, 18pt bold)

### KPI Cards (Row 1 — 7 cards)
| Card                   | Measure                   |
|------------------------|--------------------------|
| Total Patients          | [Total Patients]          |
| Total Visits            | [Total Visits]            |
| Total Treatment Cost    | [Total Treatment Cost]    |
| Avg Treatment Cost      | [Average Treatment Cost]  |
| Avg Length of Stay      | [Average Length of Stay]  |
| Avg Recovery Score      | [Average Recovery Score]  |
| High Risk %             | [High Risk %]             |

Format: Card visual, large font, border, no background

### Charts (Row 2–3)
| Position  | Chart Type  | X-Axis / Legend | Y-Axis / Values | Title                     |
|----------|------------|----------------|----------------|---------------------------|
| Top-left  | Line Chart  | visit_date (Month) | [Monthly Visits] | Monthly Patient Visits   |
| Top-right | Bar Chart   | department     | [Total Visits] | Visits by Department      |
| Bot-left  | Donut Chart | visit_type     | [Total Visits] | Visit Type Distribution   |
| Bot-right | Bar Chart   | readmission_risk | [Total Visits] | Risk Distribution         |

### Slicers (Left panel or top bar)
- `visit_date` → Date range slicer
- `department` → Dropdown / List
- `region` → Dropdown
- `gender` → Dropdown
- `age_group` → Dropdown
- `visit_type` → Dropdown

All slicers should be synced across all pages (View → Sync Slicers).

---

## PAGE 2 — Operations & Cost

### Layout
- Title: **Operations & Cost Analysis**

### KPI Cards (Row 1 — 3 cards)
| Card               | Measure                  |
|-------------------|--------------------------|
| Avg Length of Stay | [Average Length of Stay] |
| Avg Treatment Cost | [Average Treatment Cost] |
| Total Cost         | [Total Treatment Cost]   |

### Charts
| Chart Type      | Fields                                           | Title                          |
|----------------|--------------------------------------------------|-------------------------------|
| Bar (H)         | department / [Average Treatment Cost]            | Avg Cost by Department         |
| Bar (V)         | treatment_type / [Average Treatment Cost]        | Avg Cost by Treatment Type     |
| Bar (H)         | department / [Average Length of Stay]            | Avg LOS by Department          |
| Bar (V)         | visit_type / [Average Treatment Cost]            | Avg Cost by Visit Type         |
| Scatter Chart   | X = length_of_stay_days, Y = treatment_cost, Legend = department | Treatment Cost vs LOS |

### Filters
- Same slicers from Page 1 (synced)
- Additional: treatment_type slicer

---

## PAGE 3 — Patient Risk & Outcomes

### Layout
- Title: **Patient Risk & Outcomes**

### Charts
| Chart Type           | Fields                                              | Title                          |
|--------------------|-----------------------------------------------------|-------------------------------|
| Bar (Clustered V)    | readmission_risk / [Total Patients]                 | Risk Distribution              |
| Bar (Stacked H)      | department / Low Risk %, Medium Risk %, High Risk % | Risk by Department             |
| Bar (Stacked H)      | visit_type / Low Risk %, Medium Risk %, High Risk % | Risk by Visit Type             |
| Bar (H)              | department / [Average Recovery Score]               | Recovery Score by Department   |
| Scatter Chart        | X = treatment_cost, Y = recovery_score, Legend = readmission_risk | Recovery vs Cost |

### Conditional Formatting
- In the Risk Distribution chart: colour High=Red, Medium=Orange, Low=Green

### Filters (Page 3 specific)
- department
- treatment_type
- age_group
- visit_type
- region

---

## Colour Reference

| Element      | Colour  |
|-------------|---------|
| Low Risk     | #4CAF50 |
| Medium Risk  | #FF9800 |
| High Risk    | #F44336 |
| Primary blue | #3B82D4 |
| Background   | #FFFFFF |
| Surface      | #F7F8FA |
| Border       | #E5E7EB |

---

## Slicers — Recommended Visual Settings

- Style: **Dropdown** (saves space)
- Header: Show
- Multi-select: On
- Select all: On
- Font: Segoe UI, 11pt
