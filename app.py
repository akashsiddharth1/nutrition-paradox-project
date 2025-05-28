# Import necessary libraries

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# #Creating Mysql Database connection

db_connection = mysql.connector.connect(
    host='localhost',
    user='root',  
    password='998800', 
    database='nutrition_paradox'  
)
cursor = db_connection.cursor()

# Seting up Page configuration

st.set_page_config(
    page_title="Nutrition Paradox",
    page_icon="✚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and welcome text for the dashboard

st.markdown("<h1 style='text-align: center; color: black;'>🌍 Global Nutrition Analysis: Tackling Obesity and Malnutrition with WHO Data</h1>", unsafe_allow_html=True)
st.markdown("""
This project investigates the global nutritional paradox: the co-existence of undernutrition and overnutrition (obesity) across different countries, age groups, and genders using publicly available WHO (World Health Organization) data.
""")
st.divider()

# Sidebar config
st.sidebar.title("Menu") # Title of sidebar

with st.sidebar:
    st.sidebar.markdown("#### 🌍 Navigation ###") # subtitle
    selected = option_menu(
    menu_title="",
    options=["Obesity", "Malnutrition", "Combined"],
    icons=["", ""],
    menu_icon="",
    default_index=0
    )

# Load Data
@st.cache_data
def load_data(query):
    return pd.read_sql(query, db_connection)


# Execute filter

if selected == "Obesity":
    st.title("Obesity queries")
    query_option = st.selectbox("Choose a Query", [
        "Top 5 Regions in 2022",
        "Top 5 Countries with Highest Obesity",
        "Obesity Trend in India",
        "Average Obesity by Gender",
        "Country Count by Obesity Level and Age Group",
        "Top 5 Least & Most Reliable Countries",
        "Average Obesity by Age Group",
        "Consistent Low Obesity Countries",
        "Female Exceeds Male by Large Margin",
        "Global Average Per Year"
    ])

    if query_option == "Top 5 Regions in 2022":
        st.subheader(query_option)
        df = load_data("""
            SELECT Region, AVG(Mean_Estimate) AS Avg_Obesity
            FROM obesity
            WHERE Year = 2022
            GROUP BY Region
            ORDER BY Avg_Obesity DESC
            LIMIT 5
        """)
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="Region", y="Avg_Obesity", data=df, palette="coolwarm", ax=ax)
        ax.set_title("Top 5 Regions with Highest Obesity in 2022")
        st.pyplot(fig)

    elif query_option == "Top 5 Countries with Highest Obesity":
        st.subheader(query_option)
        df = load_data('''
            SELECT Country, ROUND(AVG(Mean_Estimate), 2) AS Obesity
            FROM obesity
            GROUP BY Country
            ORDER BY Obesity DESC
            LIMIT 5;
        ''')
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="Country", y="Obesity", data=df, palette="Reds_r", ax=ax)
        ax.set_title("Top 5 Countries with Highest Obesity")
        st.pyplot(fig)

    elif query_option == "Obesity Trend in India":
        st.subheader(query_option)
        df = load_data('''
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Obesity_Trend
            FROM obesity
            WHERE Country = 'India'
            GROUP BY Year
            ORDER BY Year;
        ''')
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x = "Year", y = "Obesity_Trend", data=df, palette="Set2", ax=ax)
        ax.set_title("Obesity Trend in India")
        st.pyplot(fig)

    elif query_option == "Average Obesity by Gender":
        st.subheader(query_option)
        df = load_data('''
            SELECT Gender, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            GROUP BY Gender;
        ''')
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="Gender", y="Avg_Obesity", data=df, palette="Set2", ax=ax)
        ax.set_title("Average Obesity by Gender")
        st.pyplot(fig)

    elif query_option == "Country Count by Obesity Level and Age Group":
        st.subheader(query_option)
        query = '''
            SELECT obesity_level, age_group, COUNT(DISTINCT Country) AS Country_Count
            FROM obesity
            GROUP BY obesity_level, age_group
            ORDER BY obesity_level, age_group;
        '''
        df = load_data(query)
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="obesity_level", y="Country_Count", hue="age_group", data=df, palette="viridis", ax=ax)
        ax.set_title("Country Count by Obesity Level and Age Group")
        st.pyplot(fig)

    elif query_option == "Top 5 Least & Most Reliable Countries":
        st.subheader("Top 5 Least Reliable (High CI_Width)")
        query1 = '''
            SELECT Country, ROUND(AVG(CI_Width), 2) AS Avg_CI_Width
            FROM obesity
            GROUP BY Country
            ORDER BY Avg_CI_Width DESC
            LIMIT 5;
        '''
        df1 = load_data(query1)
        st.dataframe(df1)
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df1, x="Country", y="Avg_CI_Width", palette="Reds_r", ax=ax1)
        ax1.set_title("Highest Average CI Width (Least Consistent Estimates)")
        st.pyplot(fig1)

        st.subheader("Top 5 Most Consistent (Low CI_Width)")
        query2 = '''
            SELECT Country, ROUND(AVG(CI_Width), 2) AS Avg_CI_Width
            FROM obesity
            GROUP BY Country
            ORDER BY Avg_CI_Width ASC
            LIMIT 5;
        '''
        df2 = load_data(query2)
        st.dataframe(df2)
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df2, x="Country", y="Avg_CI_Width", palette="Greens", ax=ax2)
        ax2.set_title("Lowest Average CI Width (Most Reliable Estimates)")
        st.pyplot(fig2)

    elif query_option == "Average Obesity by Age Group":
        st.subheader(query_option)
        df = load_data('''
            SELECT age_group, ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity
            FROM obesity
            GROUP BY age_group;
        ''')
        
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="age_group", y="Avg_Obesity", hue="age_group", data=df, palette="viridis", ax=ax)
        ax.set_title("Average Obesity by Age Group")
        st.pyplot(fig)

    elif query_option == "Consistent Low Obesity Countries":
        st.subheader(query_option)
        df = load_data('''
            SELECT Country, 
            ROUND(AVG(Mean_Estimate), 2) AS Avg_Obesity, 
            ROUND(AVG(CI_Width), 2) AS Avg_CI
            FROM obesity
            GROUP BY Country
            HAVING Avg_Obesity < 25 AND Avg_CI < 5
            ORDER BY Avg_Obesity ASC
            LIMIT 10;
        ''')
        
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="Country", y="Avg_Obesity", hue="Country", data=df, palette="viridis", ax=ax)
        ax.set_title("Consistent Low Obesity Countries")
        st.pyplot(fig)

    elif query_option == "Female Exceeds Male by Large Margin":
        st.subheader(query_option)
        df = load_data('''
            SELECT a.Country, a.Year, 
            a.Mean_Estimate AS Female_Obesity, 
            b.Mean_Estimate AS Male_Obesity,
            ROUND(a.Mean_Estimate - b.Mean_Estimate, 2) AS Gap
            FROM obesity a
            JOIN obesity b 
            ON a.Country = b.Country AND a.Year = b.Year
            WHERE a.Gender = 'Female' AND b.Gender = 'Male'
            AND (a.Mean_Estimate - b.Mean_Estimate) > 5
            ORDER BY Gap DESC;
        ''')
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, y='Country', x='Gap', palette='Reds_r', ax=ax)
        ax.set_title("Countries Where Female Obesity Exceeds Male by Large Margins")
        st.pyplot(fig)

    elif query_option == "Global Average Per Year":
        st.subheader(query_option)
        df = load_data('''
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Global_Avg_Obesity
            FROM obesity
            GROUP BY Year
            ORDER BY Year;
        ''')
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, y='Global_Avg_Obesity', x='Year', palette='Reds_r', ax=ax)
        ax.set_title("Global Average Per Year")
        st.pyplot(fig)


if selected == "Malnutrition":
    st.title("Malnutrition queries")
    query_option = st.selectbox("Choose a Query", [
        "Avg. malnutrition by age group",
        "Top 5 countries with highest malnutrition",
        "Malnutrition trend in African region over the years",
        "Gender-based average malnutrition",
        "Malnutrition level-wise (average CI_Width by age group)",
        "Yearly malnutrition change in specific countries(India, Nigeria, Brazil)",
        "Regions with lowest malnutrition averages",
        "Countries with increasing malnutrition",
        "Min/Max malnutrition levels year-wise comparison",
        "High CI_Width flags for monitoring"
    ])

    if query_option == "Avg. malnutrition by age group":
        st.subheader(query_option)
        df = load_data("""
            SELECT age_group, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY age_group;
        """)
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='age_group', y='Avg_Malnutrition', data=df, ci=None, palette='coolwarm', ax=ax)
        ax.set_title('Average Malnutrition by Age Group')
        st.pyplot(fig)
        

    elif query_option == "Top 5 countries with highest malnutrition":
        st.subheader(query_option)
        df = load_data("""
            SELECT Country, ROUND(AVG(Mean_Estimate), 2) AS High_Malnutrition
            FROM malnutrition
            GROUP BY Country
            ORDER BY High_Malnutrition DESC
            LIMIT 5;
        """)
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='High_Malnutrition', y='Country', data=df, palette='Reds_r', ax=ax)
        ax.set_title('Top 5 countries with highest malnutrition')
        st.pyplot(fig)

    elif query_option == "Malnutrition trend in African region over the years":
        st.subheader(query_option)
        df = load_data("""
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            WHERE Region = 'Africa'
            GROUP BY Year
            ORDER BY Year;
        """)
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x='Year', y='Avg_Malnutrition', data=df, marker='o', color='orange', ax=ax)
        ax.set_title('Malnutrition trend in African region over the years')
        st.pyplot(fig)

    elif query_option == "Gender-based average malnutrition":
        st.subheader(query_option)
        df = load_data("""
            SELECT Gender, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY Gender;
        """)
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='Gender', y='Avg_Malnutrition', data=df, palette='pastel', ax=ax)
        ax.set_title('Gender-based average malnutrition')
        st.pyplot(fig)

    elif query_option == "Malnutrition level-wise (average CI_Width by age group)":
        st.subheader(query_option)
        df = load_data("""
            SELECT malnutrition_level, age_group, ROUND(AVG(CI_Width), 2) AS Avg_CI
            FROM malnutrition
            GROUP BY malnutrition_level, age_group;
        """)
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='malnutrition_level', y='Avg_CI', hue='age_group', data=df, palette='Set2', ax=ax)
        ax.set_title('Malnutrition level-wise (average CI_Width by age group)')
        st.pyplot(fig)

    elif query_option == "Yearly malnutrition change in specific countries(India, Nigeria, Brazil)":
        st.subheader(query_option)
        df = load_data("""
            SELECT Country, Year, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            WHERE Country IN ('India', 'Nigeria', 'Brazil')
            GROUP BY Country, Year
            ORDER BY Country, Year;
        """)
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x='Year', y='Avg_Malnutrition', hue='Country', data=df, marker='o', ax=ax)
        ax.set_title('Yearly malnutrition change in specific countries(India, Nigeria, Brazil)')
        st.pyplot(fig)

    elif query_option == "Regions with lowest malnutrition averages":
        st.subheader(query_option)
        df = load_data("""
            SELECT Region, ROUND(AVG(Mean_Estimate), 2) AS Avg_Malnutrition
            FROM malnutrition
            GROUP BY Region
            ORDER BY Avg_Malnutrition ASC
            LIMIT 5;
        """)
        st.dataframe(df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='Avg_Malnutrition', y='Region', data=df, palette='Greens', ax=ax)
        ax.set_title('Regions with lowest malnutrition averages')
        st.pyplot(fig)

    elif query_option == "Countries with increasing malnutrition":
        st.subheader(query_option)
        df = load_data("""
            SELECT Country, MAX(Mean_Estimate) - MIN(Mean_Estimate) AS Increase
            FROM malnutrition
            GROUP BY Country
            HAVING Increase > 0
            ORDER BY Increase DESC;
        """)
        st.dataframe(df)
        # fig, ax = plt.subplots()
        # sns.barplot(x='Increase', y='Country', data=df, palette='Oranges', ax=ax)
        # ax.set_title('Countries with increasing malnutrition')
        # st.pyplot(fig)

        # Optional: Limit to top 20 for readability
        top_df = df.head(20)

        # Plot
        st.subheader("📈 Countries with Increasing Malnutrition Over Time")

        plt.figure(figsize=(10, 8))
        sns.barplot(data=top_df, y='Country', x='Increase', palette='rocket')
        plt.title("Top 20 Countries with Increasing Malnutrition (Max - Min)")
        plt.xlabel("Increase in Malnutrition (%)")
        plt.ylabel("Country")
        plt.tight_layout()

        # Display in Streamlit
        st.pyplot(plt)

    elif query_option == "Min/Max malnutrition levels year-wise comparison":
        st.subheader(query_option)
        df = load_data("""
            SELECT Year, 
            MIN(Mean_Estimate) AS Min_Malnutrition, 
            MAX(Mean_Estimate) AS Max_Malnutrition
            FROM malnutrition
            GROUP BY Year
            ORDER BY Year;
        """)
        st.dataframe(df)
        # fig, ax = plt.subplots()
        # sns.barplot(x='Year', y='Min_Malnutrition', data=df, palette='Oranges', ax=ax)
        # sns.barplot(x='Year', y='Max_Malnutrition', data=df, palette='Greens', ax=ax)
        # ax.set_title('Min/Max malnutrition levels year-wise comparison')
        # st.pyplot(fig)
        st.subheader("📊 Min/Max Malnutrition Rates Over the Years")

        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, x='Year', y='Min_Malnutrition', marker='o', label='Minimum')
        sns.lineplot(data=df, x='Year', y='Max_Malnutrition', marker='o', label='Maximum')
        plt.title("Min vs Max Malnutrition (Global, Year-wise)")
        plt.xlabel("Year")
        plt.ylabel("Malnutrition (%)")
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)

        
    elif query_option == "High CI_Width flags for monitoring":
        st.subheader(query_option)
        df = load_data("""
            SELECT Country, Year, CI_Width, Mean_Estimate
            FROM malnutrition
            WHERE CI_Width > 5
            ORDER BY CI_Width DESC;
        """)
        st.dataframe(df)
        # Optional: Limit to Top 500 points for performance
        df = df.head(500)

        # Plot
        st.subheader("🚨 High Confidence Interval (CI_Width > 5) in Malnutrition Estimates")

        plt.figure(figsize=(12, 6))
        scatter = sns.scatterplot(
            data=df,
            x='Year',
            y='CI_Width',
            hue='Country',
            size='CI_Width',
            palette='tab10',
            sizes=(20, 200),
            alpha=0.7,
            legend=False
        )

        plt.title("High CI_Width in Malnutrition Estimates by Year")
        plt.xlabel("Year")
        plt.ylabel("CI Width (Uncertainty in Estimate)")
        plt.grid(True)
        plt.tight_layout()

        st.pyplot(plt)

if selected == "Combined":
    st.title("🍔 Obesity vs 🧊 Malnutrition Combined Analysis")
    query_option = st.selectbox("Choose a Query", [
        "Obesity vs malnutrition comparison by country",
        "Gender-based disparity in both obesity and malnutrition",
        "Region-wise avg estimates side-by-side(Africa and America)",
        "Countries with obesity up & malnutrition down",
        "Age-wise trend analysis"
    ])

    if query_option == "Obesity vs malnutrition comparison by country":
        st.subheader("Obesity vs malnutrition comparison by country(any 5 countries)")
        countries = ['India', 'USA', 'Brazil', 'Nigeria', 'China']
        df = load_data(f"""
            SELECT Country, Year, Mean_Estimate, 'Obesity' as Type FROM obesity 
            WHERE Country IN ({','.join([f"'{c}'" for c in countries])})
            UNION ALL
            SELECT Country, Year, Mean_Estimate, 'Malnutrition' FROM malnutrition 
            WHERE Country IN ({','.join([f"'{c}'" for c in countries])})
            """)
        st.dataframe(df)
        # Plot
        st.subheader("📊 Obesity vs Malnutrition Comparison by Country")
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x='Year', y='Mean_Estimate', hue='Type', style='Country', markers=True, dashes=False)
        plt.title("Obesity vs Malnutrition Trends")
        plt.ylabel("Mean Estimate")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)

    
    elif query_option == "Gender-based disparity in both obesity and malnutrition":
        st.subheader("Gender-based disparity in both obesity and malnutrition")
        df = load_data("""
            SELECT Gender, 'Obesity' AS Type, ROUND(AVG(Mean_Estimate), 2) AS Avg_Value FROM obesity
            GROUP BY Gender
            UNION
            SELECT Gender, 'Malnutrition', ROUND(AVG(Mean_Estimate), 2) FROM malnutrition
            GROUP BY Gender;
        """)
        st.dataframe(df)
        #plot
        plt.figure(figsize=(8, 5))
        sns.barplot(data=df, x='Gender', y='Avg_Value', hue='Type')
        plt.title("Gender Disparity in Obesity vs Malnutrition")
        plt.tight_layout()
        st.pyplot(plt)


    elif query_option == "Region-wise avg estimates side-by-side(Africa and America)":
        st.subheader("Region-wise avg estimates side-by-side(Africa and America)")
        df = load_data("""
            SELECT Region, 'Obesity' AS Type, ROUND(AVG(Mean_Estimate),2) AS Avg_Est FROM obesity
            WHERE Region IN ('Africa', 'Americas')
            GROUP BY Region
            UNION
            SELECT Region, 'Malnutrition', ROUND(AVG(Mean_Estimate),2) FROM malnutrition
            WHERE Region IN ('Africa', 'Americas')
            GROUP BY Region;
        """)
        st.dataframe(df)
        #plot
        plt.figure(figsize=(8, 5))
        sns.barplot(data=df, x='Region', y='Avg_Est', hue='Type')
        plt.title("Obesity vs Malnutrition by Region")
        plt.tight_layout()
        st.pyplot(plt)


    elif query_option == "Countries with obesity up & malnutrition down":
        st.subheader("Countries with obesity up & malnutrition down")
        df = load_data("""
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
        WHERE o.avg_obesity >= 25   
          AND m.avg_malnutrition < 10;  
        """)
        st.dataframe(df)
        #plot
        plt.figure(figsize=(10, 5))
        sns.scatterplot(data=df, x='avg_obesity', y='avg_malnutrition', hue='Country', s=100)
        plt.title("Countries: Obesity Up, Malnutrition Down")
        plt.xlabel("Obesity Increase")
        plt.ylabel("Malnutrition Decrease")
        plt.tight_layout()
        st.pyplot(plt)

    
    elif query_option == "Age-wise trend analysis":
        st.subheader("Age-wise trend analysis")
        df = load_data("""
            SELECT Year, Age_Group, 'Obesity' AS Type, ROUND(AVG(Mean_Estimate), 2) AS Avg_Est FROM obesity
            GROUP BY Year, Age_Group
            UNION
            SELECT Year, Age_Group, 'Malnutrition', ROUND(AVG(Mean_Estimate), 2) FROM malnutrition
            GROUP BY Year, Age_Group;
        """)
        st.dataframe(df)
        #plot
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='Year', y='Avg_Est', hue='Type', style='Age_Group')
        plt.title("Trend by Age Group in Obesity vs Malnutrition")
        plt.tight_layout()
        st.pyplot(plt)
