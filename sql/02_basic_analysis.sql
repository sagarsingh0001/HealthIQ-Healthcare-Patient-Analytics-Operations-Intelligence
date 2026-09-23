-- =============================================================
-- HealthIQ — Healthcare Patient Analytics
-- 02_basic_analysis.sql
-- Purpose: Patient demographics and visit overview
-- =============================================================

-- Q1. How many unique patients are there?
SELECT COUNT(DISTINCT patient_id) AS unique_patients
FROM patient_data;

-- Q2. How many total visits are there?
SELECT COUNT(*) AS total_visits
FROM patient_data;

-- Q3. Which departments receive the most visits?
SELECT
    department,
    COUNT(*) AS total_visits,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patient_data), 2) AS pct_of_total
FROM patient_data
GROUP BY department
ORDER BY total_visits DESC;

-- Q4. Which regions have the most patients?
SELECT
    region,
    COUNT(*) AS total_patients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patient_data), 2) AS pct_of_total
FROM patient_data
GROUP BY region
ORDER BY total_patients DESC;

-- Q5. What is the distribution of visit types?
SELECT
    visit_type,
    COUNT(*) AS total_visits,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patient_data), 2) AS pct_of_total
FROM patient_data
GROUP BY visit_type
ORDER BY total_visits DESC;

-- Q5b. Age group distribution
SELECT
    age_group,
    COUNT(*) AS total_patients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patient_data), 2) AS pct_of_total
FROM patient_data
GROUP BY age_group
ORDER BY FIELD(age_group, '18-30', '31-45', '46-60', '60+');

-- Q5c. Gender distribution
SELECT
    gender,
    COUNT(*) AS total_patients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM patient_data), 2) AS pct_of_total
FROM patient_data
GROUP BY gender
ORDER BY total_patients DESC;

-- Q5d. Monthly patient visit trend
SELECT
    DATE_FORMAT(visit_date, '%Y-%m') AS visit_month,
    COUNT(*) AS total_visits
FROM patient_data
GROUP BY visit_month
ORDER BY visit_month;
