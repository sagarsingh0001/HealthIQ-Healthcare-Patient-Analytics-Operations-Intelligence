-- =============================================================
-- HealthIQ — Healthcare Patient Analytics
-- 04_cost_analysis.sql
-- Purpose: Treatment cost and financial analysis
-- =============================================================

-- Q6. What is the total treatment cost?
SELECT
    ROUND(SUM(treatment_cost), 2)  AS total_cost,
    ROUND(AVG(treatment_cost), 2)  AS avg_cost,
    ROUND(MIN(treatment_cost), 2)  AS min_cost,
    ROUND(MAX(treatment_cost), 2)  AS max_cost
FROM patient_data;

-- Q7. Average treatment cost
SELECT ROUND(AVG(treatment_cost), 2) AS avg_treatment_cost
FROM patient_data;

-- Q8. Which departments have the highest average treatment cost?
SELECT
    department,
    ROUND(AVG(treatment_cost), 2) AS avg_cost,
    ROUND(SUM(treatment_cost), 2) AS total_cost,
    COUNT(*)                      AS visits
FROM patient_data
GROUP BY department
ORDER BY avg_cost DESC;

-- Q9. Which treatment types are the most expensive?
SELECT
    treatment_type,
    ROUND(AVG(treatment_cost), 2) AS avg_cost,
    ROUND(SUM(treatment_cost), 2) AS total_cost,
    COUNT(*)                      AS visits
FROM patient_data
GROUP BY treatment_type
ORDER BY avg_cost DESC;

-- Q10. What is the average cost by visit type?
SELECT
    visit_type,
    ROUND(AVG(treatment_cost), 2) AS avg_cost,
    ROUND(SUM(treatment_cost), 2) AS total_cost,
    COUNT(*)                      AS visits
FROM patient_data
GROUP BY visit_type
ORDER BY avg_cost DESC;

-- Cost by region
SELECT
    region,
    ROUND(AVG(treatment_cost), 2) AS avg_cost,
    ROUND(SUM(treatment_cost), 2) AS total_cost,
    COUNT(*)                      AS visits
FROM patient_data
GROUP BY region
ORDER BY total_cost DESC;

-- Cost by age group
SELECT
    age_group,
    ROUND(AVG(treatment_cost), 2) AS avg_cost,
    ROUND(SUM(treatment_cost), 2) AS total_cost,
    COUNT(*)                      AS visits
FROM patient_data
GROUP BY age_group
ORDER BY FIELD(age_group, '18-30', '31-45', '46-60', '60+');

-- CTE: Classify costs as Low / Medium / High and count
WITH cost_tiers AS (
    SELECT
        patient_id,
        treatment_cost,
        CASE
            WHEN treatment_cost < 35000  THEN 'Low (<$35k)'
            WHEN treatment_cost < 70000  THEN 'Medium ($35k–$70k)'
            ELSE                              'High (>$70k)'
        END AS cost_tier
    FROM patient_data
)
SELECT
    cost_tier,
    COUNT(*)                                                  AS visits,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patient_data), 2) AS pct
FROM cost_tiers
GROUP BY cost_tier
ORDER BY FIELD(cost_tier, 'Low (<$35k)', 'Medium ($35k–$70k)', 'High (>$70k)');

-- Department × treatment type average cost
SELECT
    department,
    treatment_type,
    ROUND(AVG(treatment_cost), 2) AS avg_cost,
    COUNT(*)                      AS visits
FROM patient_data
GROUP BY department, treatment_type
ORDER BY department, avg_cost DESC;

-- Window function: rank departments by avg cost
SELECT
    department,
    ROUND(AVG(treatment_cost), 2)                                                          AS avg_cost,
    RANK() OVER (ORDER BY ROUND(AVG(treatment_cost), 2) DESC)                              AS cost_rank
FROM patient_data
GROUP BY department;
