import pandas as pd

# Create sales data
sales_data = {
    'Date': ['2025-01-05', '2025-01-05', '2025-01-05', '2025-01-12', '2025-01-12',
             '2025-01-12', '2025-01-19', '2025-01-19', '2025-01-19', '2025-01-26',
             '2025-01-26', '2025-01-26'],
    'Store': ['A1', 'B2', 'C3', 'A1', 'D4', 'E5', 'F6', 'G7', 'H8', 'B2', 'C3', 'E5'],
    'Region': ['North', 'South', 'North', 'North', 'West', 'East', 'West', 'North',
               'East', 'South', 'North', 'East'],
    'Sales': [1250, 800, 2100, 1350, None, 1850, 1500, 3500, 1050, 900, 2200, 1900],
    'ItemsSold': [80, 55, 120, 85, 60, 110, 95, 200, 70, 65, 130, 115]
}

# Create stores data
stores_data = {
    'Store': ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8'],
    'Type': ['Urban', 'Suburban', 'Urban', 'Rural', 'Suburban', 'Rural', 'Urban', 'Suburban'],
    'StaffSize': [12, 8, 18, 9, 15, 11, 28, 10],
    'SquareFootage': [1500, 1200, 2500, 1300, 2000, 1400, 3500, 1800]
}

# Save to CSV
df_sales_raw = pd.DataFrame(sales_data)
df_stores_raw = pd.DataFrame(stores_data)

df_sales_raw.to_csv('sales.csv', index=False)
df_stores_raw.to_csv('stores.csv', index=False)

print("Files 'sales.csv' and 'stores.csv' created successfully.")