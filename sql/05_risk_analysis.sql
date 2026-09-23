-- =============================================================
-- HealthIQ — Healthcare Patient Analytics
-- 05_risk_analysis.sql
-- Purpose: Readmission risk and outcome analysis
-- =============================================================

-- Q17. What percentage of patients are High, Medium, Low risk?
SELECT
    readmission_risk,
    COUNT(*)                                                          AS patients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patient_data), 2) AS pct
FROM patient_data
GROUP BY readmission_risk
ORDER BY FIELD(readmission_risk, 'High', 'Medium', 'Low');

-- Q18. Which departments have the highest High-Risk percentage?
SELECT
    department,
    COUNT(*)                                                             AS total_visits,
    SUM(CASE WHEN readmission_risk = 'High' THEN 1 ELSE 0 END)         AS high_risk_count,
    ROUND(
        SUM(CASE WHEN readmission_risk = 'High' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    )                                                                    AS high_risk_pct
FROM patient_data
GROUP BY department
ORDER BY high_risk_pct DESC;

-- Q19. How does risk vary by visit type?
SELECT
    visit_type,
    readmission_risk,
    COUNT(*)                                                                AS patients,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY visit_type), 2) AS pct_within_visit_type
FROM patient_data
GROUP BY visit_type, readmission_risk
ORDER BY visit_type, FIELD(readmission_risk, 'High', 'Medium', 'Low');

-- Q20. How does risk vary by age group?
SELECT
    age_group,
    readmission_risk,
    COUNT(*)                                                                  AS patients,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY age_group), 2) AS pct_within_age_group
FROM patient_data
GROUP BY age_group, readmission_risk
ORDER BY FIELD(age_group, '18-30', '31-45', '46-60', '60+'),
         FIELD(readmission_risk, 'High', 'Medium', 'Low');

-- Risk by treatment type
SELECT
    treatment_type,
    readmission_risk,
    COUNT(*) AS patients,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY treatment_type), 2) AS pct_within_treatment
FROM patient_data
GROUP BY treatment_type, readmission_risk
ORDER BY treatment_type, FIELD(readmission_risk, 'High', 'Medium', 'Low');

-- Risk by region
SELECT
    region,
    readmission_risk,
    COUNT(*) AS patients,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY region), 2) AS pct_within_region
FROM patient_data
GROUP BY region, readmission_risk
ORDER BY region, FIELD(readmission_risk, 'High', 'Medium', 'Low');

-- Average recovery score by risk category
SELECT
    readmission_risk,
    ROUND(AVG(recovery_score),       2) AS avg_recovery,
    ROUND(AVG(treatment_cost),       2) AS avg_cost,
    ROUND(AVG(length_of_stay_days),  2) AS avg_los,
    COUNT(*)                            AS patients
FROM patient_data
GROUP BY readmission_risk
ORDER BY FIELD(readmission_risk, 'High', 'Medium', 'Low');

-- CTE: High-risk patients with high cost — identify combined risk
WITH high_burden AS (
    SELECT
        patient_id,
        department,
        treatment_type,
        treatment_cost,
        recovery_score,
        length_of_stay_days,
        readmission_risk
    FROM patient_data
    WHERE readmission_risk = 'High'
      AND treatment_cost > 70000
)
SELECT
    department,
    COUNT(*)                           AS high_burden_patients,
    ROUND(AVG(treatment_cost), 2)      AS avg_cost,
    ROUND(AVG(recovery_score), 2)      AS avg_recovery,
    ROUND(AVG(length_of_stay_days), 2) AS avg_los
FROM high_burden
GROUP BY department
ORDER BY high_burden_patients DESC;
