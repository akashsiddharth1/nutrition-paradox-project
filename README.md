# nutrition-paradox-project
🌍 Global Nutrition Analysis: Tackling Obesity and Malnutrition with WHO Data This project investigates the global nutritional paradox: the co-existence of undernutrition and overnutrition (obesity) across different countries, age groups, and genders using publicly available WHO (World Health Organization) data.

🗂️ Project Overview We extract, clean, analyze, and visualize global obesity and malnutrition trends between 2012 and 2022, then insert the cleaned data into a MySQL database for long-term storage and querying.

🛠️ Step-by-Step Workflow

📥 Data Collection from WHO API We use 4 WHO public API endpoints:
Indicator API URL (WHO) Obesity (Adults) https://ghoapi.azureedge.net/api/NCD_BMI_30C Obesity (Children) https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C Malnutrition (Adults) https://ghoapi.azureedge.net/api/NCD_BMI_18C Malnutrition (Children) https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C

🧹 Data Preprocessing & Cleaning Loaded data from APIs using requests and converted JSON into DataFrames.
Filtered records from 2012 to 2022.

Selected relevant columns:

ParentLocation, Dim1, TimeDim, Low, High, NumericValue, SpatialDim

Renamed columns for clarity:

TimeDim → Year, Dim1 → Gender, NumericValue → Mean_Estimate, etc.

Standardized Gender labels to 'Male', 'Female', and 'Both'.

Merged datasets:

df_obesity: Combined adult and child obesity datasets.

df_malnutrition: Combined adult and child malnutrition datasets.

Created age_group column manually to distinguish between Adult and Child/Adolescent.

Converted 3-letter country codes to full country names using the pycountry package.

Handled regional placeholders like 'AFR', 'GLOBAL', etc. using a special dictionary.

Calculated Confidence Interval Width:

CI_Width = UpperBound - LowerBound

Created new classification columns:

obesity_level: Low, Moderate, High (based on BMI value)

malnutrition_level: Low, Moderate, High (based on underweight %)

📊 Exploratory Data Analysis (EDA) Using Pandas, Matplotlib, and Seaborn, we explored:
Distribution of obesity and malnutrition across years, genders, and regions

Line plots to observe trends over time

Boxplots to analyze variability by gender and age group

Bar plots to compare top/bottom affected regions

Heatmaps and scatter plots for pattern detection

💽 Data Insertion into MySQL Used mysql.connector to connect to a local MySQL server.
Created two SQL tables: obesity and malnutrition

Inserted cleaned records from Pandas DataFrames into MySQL using .iterrows() loop.

🔍 Key Findings Adult obesity is rising steadily, especially among males in high-income regions.

Children in low-income regions continue to face high levels of thinness/malnutrition.

Gender differences are apparent in both nutritional extremes.

Global strategies must balance overnutrition policies in developed countries and malnutrition interventions in developing regions.

📦 Technologies Used Python (Pandas, Seaborn, Matplotlib, Requests, Pycountry)

MySQL for relational data storage

WHO API for real-time health data
