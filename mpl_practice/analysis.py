import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Setup and Data Preparation ---

# Task 1.2: Load DataFrames
# Parsing dates immediately upon load
df_sales = pd.read_csv('sales.csv', parse_dates=['Date'])
df_stores = pd.read_csv('stores.csv')

# Task 1.2: Data Cleaning (Missing Values)
# Calculate mean of Sales (numeric_only=True is good practice)
sales_mean = df_sales['Sales'].mean(numeric_only=True)

# Fill missing values.
# Note: We use inplace=True as requested, though assigning back (df = df.fillna) is also common.
df_sales['Sales'] = df_sales['Sales'].fillna(sales_mean)

print("--- Data Cleaned (Missing Sales filled) ---")
print(df_sales.head(), "\n")


# --- 2. Core Data Exploration ---

# Task 2.1: Sorting
sorted_sales = df_sales.sort_values(by='Sales', ascending=False)

# Task 2.1: Limiting (Top 3)
top_3_sales = sorted_sales.head(3)
print("--- Top 3 Sales Records ---")
print(top_3_sales, "\n")

# Task 2.1: Conditional Filter (North Region)
north_sales = df_sales[df_sales['Region'] == 'North']
print("--- North Region Records ---")
print(north_sales.head(), "\n")

# Task 2.2: Descriptive Statistics
print("--- Statistical Summary ---")
print(df_sales.describe(), "\n")

mean_sales = df_sales['Sales'].mean()
max_items = df_sales['ItemsSold'].max()
print(f"Mean Sales: {mean_sales:.2f}")
print(f"Max Items Sold: {max_items}\n")

# Task 2.3: Creating New Columns (Feature Engineering)
df_sales['SalesPerItem'] = df_sales['Sales'] / df_sales['ItemsSold']

# Find store with highest SalesPerItem
# We locate the row with the max value in the new column
max_spi_row = df_sales.loc[df_sales['SalesPerItem'].idxmax()]
print("--- Highest Sales Per Item ---")
print(f"Store: {max_spi_row['Store']} | Value: {max_spi_row['SalesPerItem']:.2f}\n")


# --- 3. Advanced Analysis and Visualization ---

# Task 3.1: Joining DataFrames
# Inner join on 'Store'
merged_df = pd.merge(df_sales, df_stores, on='Store', how='inner')

# Task 3.2: Grouping and Aggregation
region_stats = merged_df.groupby('Region').agg({
    'Sales': 'sum',
    'StaffSize': 'mean'
})

print("--- Aggregated Stats by Region ---")
print(region_stats, "\n")

# Task 3.3: Data Visualization

# Task 3.3: Data Visualization

# Bar Chart: Total Sales per Region
plt.figure(figsize=(10, 6))
region_stats['Sales'].plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# CHANGE: Save instead of show
plt.savefig('regional_sales_bar_chart.png') 
print("Bar chart saved to 'regional_sales_bar_chart.png'")
plt.close() # Close the plot to free up memory

# Scatter Plot: StaffSize vs Sales
plt.figure(figsize=(10, 6))
plt.scatter(merged_df['StaffSize'], merged_df['Sales'], color='green', alpha=0.7, s=100)
plt.title('Relationship: Staff Size vs Sales')
plt.xlabel('Staff Size')
plt.ylabel('Sales ($)')
plt.grid(True, linestyle='--', alpha=0.5)

# CHANGE: Save instead of show
plt.savefig('staff_sales_scatter.png')
print("Scatter plot saved to 'staff_sales_scatter.png'")
plt.close()