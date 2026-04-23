# datasciencetoolbox-python
Code of Dashboard written in python 
🌍 Air Pollution & Greenhouse Gas Analysis Dashboard
📌 Project Overview

This project focuses on analyzing global air pollutants and greenhouse gas emissions over time using Python. The goal is to understand pollution trends, compare countries, and derive meaningful insights through interactive visualizations.

🎯 Objectives
Analyze trends of air pollutants across years
Compare pollution levels between countries
Study relationships between pollutants and greenhouse gases
Create an interactive dashboard for better visualization
📊 Dataset

The datasets used in this project are sourced from Our World in Data:

Methane Emissions Dataset
CO₂ Emissions per Capita Dataset
Long-run Air Pollution Dataset
🧹 Data Preprocessing
Removed unnecessary records (e.g., World data)
Handled missing values
Merged multiple datasets using common columns (Entity, Year)
Renamed columns for clarity
Created a new feature: Average Pollution Index
🛠️ Technologies Used
Python
Pandas & NumPy (Data processing)
Seaborn & Matplotlib (Statistical visualization)
hvPlot (Interactive plotting)
Panel (Dashboard development)
📈 Visualizations Included
📊 Bar Chart → Top polluted countries
📉 Histogram → Distribution of pollutants with KDE
🔵 Scatter Plot → CO₂ vs Pollution
🔥 Heatmap → Correlation analysis
🥧 Pie Chart → Pollutant contribution
📦 Box Plot → Distribution & outliers
🔗 Pairplot → Relationship between variables
⚙️ Features
Interactive Year Slider
Country Dropdown Filter
Dynamic Pollutant Selection
Real-time updating visualizations
📌 Key Insights
Pollution trends vary significantly across countries
Strong relationships exist between certain pollutants
Distribution analysis reveals skewness and outliers in data
CO₂ and Methane contribute significantly to environmental impact
