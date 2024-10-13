import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

# Load dataset
df = pd.read_csv('Imports_Exports_Dataset.csv')
sample = df.sample(n=3001, random_state=55055)

# Convert 'Date' to datetime and extract Month/Year
sample['Date'] = pd.to_datetime(sample['Date'])
sample['Month'] = sample['Date'].dt.to_period('M')

# Title of the Dashboard
st.title("Import Export Dashboard")

# Sidebar Slicers
st.sidebar.header("Filters")
# Date Range Filter
start_date = st.sidebar.date_input("Start Date", sample['Date'].min())
end_date = st.sidebar.date_input("End Date", sample['Date'].max())
# Country Filter
countries = st.sidebar.multiselect("Select Countries", sample['Country'].unique(), default=sample['Country'].unique())
# Product Category Filter
categories = st.sidebar.multiselect("Select Categories", sample['Category'].unique(), default=sample['Category'].unique())

# 1. Line Graph: Total Value of Imports and Exports Over Time
st.subheader("Total Values of Imports and Exports Over Time")
monthly_data = sample.groupby(['Month', 'Import_Export'])['Value'].sum().unstack()
fig, ax = plt.subplots(figsize=(10, 6))
monthly_data.plot(kind='line', marker='o', ax=ax)
ax.set_title('Imports vs Exports Over Time')
ax.set_xlabel('Month')
ax.set_ylabel('Transaction Value')
st.pyplot(fig)

# 2. Bar Chart: Country with the Highest Quantity of Exports
st.subheader("Country with the Highest Quantity of Exports")
sample_export = sample[sample['Import_Export'] == 'Export']
sample_export_grouped = sample_export.groupby('Country')['Quantity'].sum().reset_index()
top_10_exporting_countries = sample_export_grouped.sort_values(by='Quantity', ascending=False).head(10)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_10_exporting_countries, x='Country', y='Quantity', ax=ax)
ax.set_title('Top 10 Countries by Export Quantity')
plt.xticks(rotation=45)
st.pyplot(fig)

# 3. Pie Chart: Distribution of Shipping Methods
st.subheader("Distribution of Shipping Methods")
shipping_method_counts = sample['Shipping_Method'].value_counts()
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(shipping_method_counts, labels=shipping_method_counts.index, autopct='%1.1f%%')
ax.set_title('Distribution of Shipping Methods')
st.pyplot(fig)

# 4. Bar Chart: Top Export Product Categories by Value
st.subheader("Top Export Product Categories by Value")
sample_export_grouped = sample_export.groupby('Category')['Value'].sum().reset_index().sort_values(by='Value', ascending=False)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=sample_export_grouped, x='Category', y='Value', ax=ax)
ax.set_title('Top Export Product Categories by Value')
plt.xticks(rotation=45)
st.pyplot(fig)

# 5. Heatmap: Correlation Between Numerical Variables
st.subheader("Correlation Between Numerical Variables")
numeric_cols = ['Quantity', 'Value', 'Weight', 'Customs_Code']
correlation_matrix = sample[numeric_cols].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Correlation Between Numerical Variables')
st.pyplot(fig)

# 6. Bar Chart: Top 5 Customers by Total Purchase Value
st.subheader("Top 5 Customers by Total Purchase Value")
sample_customers = sample.groupby('Customer')['Value'].sum().reset_index().sort_values(by='Value', ascending=False).head(5)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=sample_customers, x='Customer', y='Value', ax=ax)
ax.set_title('Top 5 Customers by Total Purchase Value')
st.pyplot(fig)

# 7. Histogram: Distribution of Shipping Weight
st.subheader("Distribution of Shipping Weight")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(sample['Weight'], bins=20, kde=True, ax=ax)
ax.set_title('Distribution of Shipping Weight')
st.pyplot(fig)
