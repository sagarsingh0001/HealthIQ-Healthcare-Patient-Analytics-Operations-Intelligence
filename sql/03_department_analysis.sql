-- =============================================================
-- HealthIQ — Healthcare Patient Analytics
-- 03_department_analysis.sql
-- Purpose: Department and operational analysis
-- =============================================================

-- Q11. What is the average length of stay?
SELECT ROUND(AVG(length_of_stay_days), 2) AS avg_los_days
FROM patient_data;

-- Q12. Which departments have the longest average length of stay?
SELECT
    department,
    ROUND(AVG(length_of_stay_days), 2) AS avg_los,
    ROUND(MIN(length_of_stay_days), 2) AS min_los,
    ROUND(MAX(length_of_stay_days), 2) AS max_los,
    COUNT(*)                           AS total_visits
FROM patient_data
GROUP BY department
ORDER BY avg_los DESC;

-- Q13. Which visit types have the longest length of stay?
SELECT
    visit_type,
    ROUND(AVG(length_of_stay_days), 2) AS avg_los,
    COUNT(*)                           AS total_visits
FROM patient_data
GROUP BY visit_type
ORDER BY avg_los DESC;

-- Department × visit type breakdown
SELECT
    department,
    visit_type,
    ROUND(AVG(length_of_stay_days), 2) AS avg_los,
    COUNT(*)                           AS visits
FROM patient_data
GROUP BY department, visit_type
ORDER BY department, visit_type;

-- Q14. What is the average recovery score?
SELECT ROUND(AVG(recovery_score), 2) AS avg_recovery_score
FROM patient_data;

-- Q15. Which departments have the highest recovery score?
SELECT
    department,
    ROUND(AVG(recovery_score), 2) AS avg_recovery,
    ROUND(MIN(recovery_score), 2) AS min_recovery,
    ROUND(MAX(recovery_score), 2) AS max_recovery
FROM patient_data
GROUP BY department
ORDER BY avg_recovery DESC;

-- Q16. Which treatments have the highest recovery score?
SELECT
    treatment_type,
    ROUND(AVG(recovery_score), 2) AS avg_recovery,
    COUNT(*)                       AS total_visits
FROM patient_data
GROUP BY treatment_type
ORDER BY avg_recovery DESC;

-- Department × treatment type: volume
SELECT
    department,
    treatment_type,
    COUNT(*) AS visits
FROM patient_data
GROUP BY department, treatment_type
ORDER BY department, visits DESC;
