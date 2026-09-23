-- =============================================================
-- HealthIQ — Healthcare Patient Analytics
-- 01_data_quality.sql
-- Purpose: Verify data quality of the loaded dataset
-- =============================================================

-- 1. Total row count
SELECT COUNT(*) AS total_rows
FROM patient_data;

-- 2. Unique patients
SELECT COUNT(DISTINCT patient_id) AS unique_patients
FROM patient_data;

-- 3. Check for NULL values in each column
SELECT
    SUM(CASE WHEN patient_id           IS NULL THEN 1 ELSE 0 END) AS null_patient_id,
    SUM(CASE WHEN visit_date           IS NULL THEN 1 ELSE 0 END) AS null_visit_date,
    SUM(CASE WHEN age_group            IS NULL THEN 1 ELSE 0 END) AS null_age_group,
    SUM(CASE WHEN gender               IS NULL THEN 1 ELSE 0 END) AS null_gender,
    SUM(CASE WHEN region               IS NULL THEN 1 ELSE 0 END) AS null_region,
    SUM(CASE WHEN department           IS NULL THEN 1 ELSE 0 END) AS null_department,
    SUM(CASE WHEN treatment_type       IS NULL THEN 1 ELSE 0 END) AS null_treatment_type,
    SUM(CASE WHEN visit_type           IS NULL THEN 1 ELSE 0 END) AS null_visit_type,
    SUM(CASE WHEN length_of_stay_days  IS NULL THEN 1 ELSE 0 END) AS null_los,
    SUM(CASE WHEN treatment_cost       IS NULL THEN 1 ELSE 0 END) AS null_cost,
    SUM(CASE WHEN recovery_score       IS NULL THEN 1 ELSE 0 END) AS null_recovery,
    SUM(CASE WHEN readmission_risk     IS NULL THEN 1 ELSE 0 END) AS null_risk
FROM patient_data;

-- 4. Check for invalid numeric values
SELECT
    SUM(CASE WHEN length_of_stay_days < 0 THEN 1 ELSE 0 END) AS negative_los,
    SUM(CASE WHEN treatment_cost      < 0 THEN 1 ELSE 0 END) AS negative_cost,
    SUM(CASE WHEN recovery_score      < 0 OR recovery_score > 100 THEN 1 ELSE 0 END) AS invalid_recovery
FROM patient_data;

-- 5. Check distinct values in categorical columns
SELECT DISTINCT age_group    FROM patient_data ORDER BY age_group;
SELECT DISTINCT gender       FROM patient_data ORDER BY gender;
SELECT DISTINCT region       FROM patient_data ORDER BY region;
SELECT DISTINCT department   FROM patient_data ORDER BY department;
SELECT DISTINCT treatment_type FROM patient_data ORDER BY treatment_type;
SELECT DISTINCT visit_type   FROM patient_data ORDER BY visit_type;
SELECT DISTINCT readmission_risk FROM patient_data ORDER BY readmission_risk;

-- 6. Date range
SELECT
    MIN(visit_date) AS earliest_visit,
    MAX(visit_date) AS latest_visit
FROM patient_data;

-- 7. Numeric summary
SELECT
    ROUND(MIN(length_of_stay_days),  2) AS min_los,
    ROUND(MAX(length_of_stay_days),  2) AS max_los,
    ROUND(AVG(length_of_stay_days),  2) AS avg_los,
    ROUND(MIN(treatment_cost),       2) AS min_cost,
    ROUND(MAX(treatment_cost),       2) AS max_cost,
    ROUND(AVG(treatment_cost),       2) AS avg_cost,
    ROUND(MIN(recovery_score),       2) AS min_recovery,
    ROUND(MAX(recovery_score),       2) AS max_recovery,
    ROUND(AVG(recovery_score),       2) AS avg_recovery
FROM patient_data;
