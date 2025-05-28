create database nutrition_paradox;

SELECT * from nutrition_paradox.malnutrition;

select * from nutrition_paradox.obesity;

SELECT VERSION();



-- 📘 Obesity Table Queries --

-- 1. Top 5 regions with highest average obesity levels in 2022 --
SELECT Region, AVG(Mean_Estimate) AS avg_obesity
FROM obesity
WHERE Year = 2022
GROUP BY Region
ORDER BY avg_obesity DESC
LIMIT 5;

-- 2. Top 5 countries with highest obesity estimates
SELECT Country, MAX(Mean_Estimate) AS max_obesity
FROM obesity
GROUP BY Country
ORDER BY max_obesity DESC
LIMIT 5;

-- 3. Obesity trend in India over the years
SELECT Year, AVG(Mean_Estimate) AS avg_obesity
FROM obesity
WHERE Country = 'India'
GROUP BY Year;

-- 4. Average obesity by gender
SELECT Gender, AVG(Mean_Estimate) AS avg_obesity
FROM obesity
GROUP BY Gender;

-- 5. Country count by obesity level category and age group
SELECT obesity_level, age_group, COUNT(DISTINCT Country) AS country_count
FROM obesity
GROUP BY obesity_level, age_group;

-- 6. Countries with highest and lowest average CI_Width
(SELECT Country, AVG(CI_Width) AS avg_ci FROM obesity GROUP BY Country ORDER BY avg_ci DESC LIMIT 5)
UNION ALL
(SELECT Country, AVG(CI_Width) AS avg_ci FROM obesity GROUP BY Country ORDER BY avg_ci ASC LIMIT 5);

-- 7. Average obesity by age group
SELECT age_group, AVG(Mean_Estimate) AS avg_obesity FROM obesity GROUP BY age_group;

-- 8. Countries with consistent low obesity
SELECT Country, AVG(Mean_Estimate) AS avg_obesity, AVG(CI_Width) AS avg_ci
FROM obesity
GROUP BY Country
HAVING avg_obesity < 25 AND avg_ci < 2
ORDER BY avg_obesity ASC
LIMIT 10;

-- 9. Countries where female obesity exceeds male by large margin (same year)
SELECT a.Country, a.Year, a.Mean_Estimate AS female_obesity, b.Mean_Estimate AS male_obesity,
       (a.Mean_Estimate - b.Mean_Estimate) AS gap
FROM obesity a
JOIN obesity b ON a.Country = b.Country AND a.Year = b.Year
WHERE a.Gender = 'Female' AND b.Gender = 'Male'
  AND (a.Mean_Estimate - b.Mean_Estimate) > 10;

-- 10. Global average obesity percentage per year
SELECT Year, AVG(Mean_Estimate) AS global_avg_obesity FROM obesity GROUP BY Year;



-- 📘 Malnutrition Table Queries --

-- 1. Avg. malnutrition by age group
SELECT age_group, AVG(Mean_Estimate) AS avg_malnutrition FROM malnutrition GROUP BY age_group;

-- 2. Top 5 countries with highest malnutrition
SELECT Country, MAX(Mean_Estimate) AS max_malnutrition FROM malnutrition GROUP BY Country ORDER BY max_malnutrition DESC LIMIT 5;

-- 3. Malnutrition trend in African region
SELECT Year, AVG(Mean_Estimate) AS avg_malnutrition FROM malnutrition WHERE Region = 'Africa' GROUP BY Year;

-- 4. Gender-based average malnutrition
SELECT Gender, AVG(Mean_Estimate) AS avg_malnutrition FROM malnutrition GROUP BY Gender;

-- 5. Malnutrition level-wise (average CI_Width by age group)
SELECT malnutrition_level, age_group, AVG(CI_Width) AS avg_ci FROM malnutrition GROUP BY malnutrition_level, age_group;

-- 6. Yearly malnutrition change in India, Nigeria, Brazil
SELECT Country, Year, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition
WHERE Country IN ('India', 'Nigeria', 'Brazil')
GROUP BY Country, Year;

-- 7. Regions with lowest malnutrition averages
SELECT Region, AVG(Mean_Estimate) AS avg_malnutrition FROM malnutrition GROUP BY Region ORDER BY avg_malnutrition ASC LIMIT 5;

-- 8. Countries with increasing malnutrition
SELECT Country, MAX(Mean_Estimate) - MIN(Mean_Estimate) AS increase
FROM malnutrition
GROUP BY Country
HAVING increase > 0
ORDER BY increase DESC;

-- 9. Min/Max malnutrition levels year-wise
SELECT Year, MIN(Mean_Estimate) AS min_val, MAX(Mean_Estimate) AS max_val FROM malnutrition GROUP BY Year;

-- 10. High CI_Width flags
SELECT * FROM malnutrition WHERE CI_Width > 5;



-- 📘 Combined Queries --

-- 1. Obesity vs malnutrition by country (5 countries)
SELECT o.Country, o.Year, o.Mean_Estimate AS obesity, m.Mean_Estimate AS malnutrition
FROM obesity o
JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
WHERE o.Country IN ('India', 'USA', 'Brazil', 'Nigeria', 'Indonesia');

-- 2. Gender-based disparity in both obesity and malnutrition
SELECT 'Obesity' AS metric, Gender, AVG(Mean_Estimate) AS avg_value FROM obesity GROUP BY Gender
UNION ALL
SELECT 'Malnutrition', Gender, AVG(Mean_Estimate) FROM malnutrition GROUP BY Gender;

-- 3. Region-wise average estimates (Africa and America)
SELECT Region, 'Obesity' AS metric, AVG(Mean_Estimate) AS avg_val FROM obesity WHERE Region IN ('Africa', 'Americas') GROUP BY Region
UNION ALL
SELECT Region, 'Malnutrition', AVG(Mean_Estimate) FROM malnutrition WHERE Region IN ('Africa', 'Americas') GROUP BY Region;

-- 4. Countries where obesity up & malnutrition down
SELECT o.Country,
       o.avg_obesity,
       m.avg_malnutrition
FROM (
    SELECT Country, AVG(Mean_Estimate) AS avg_obesity
    FROM obesity
    GROUP BY Country
) o
JOIN (
    SELECT Country, AVG(Mean_Estimate) AS avg_malnutrition
    FROM malnutrition
    GROUP BY Country
) m ON o.Country = m.Country
WHERE o.avg_obesity >= 25   -- Moderate to High obesity
  AND m.avg_malnutrition < 10;  -- Low malnutrition



-- 5. Age-wise trend analysis
SELECT Year, age_group, AVG(Mean_Estimate) AS avg_obesity FROM obesity GROUP BY Year, age_group
UNION ALL
SELECT Year, age_group, AVG(Mean_Estimate) AS avg_malnutrition FROM malnutrition GROUP BY Year, age_group;
