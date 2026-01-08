import sqlite3
import pandas as pd

# Load your CSVs
df_sales = pd.read_csv('sales_regional.csv')
df_products = pd.read_csv('products_regional.csv')
df_stores = pd.read_csv('stores_regional.csv')
df_plano = pd.read_csv('plano_regional.csv')

# Create a database connection
conn = sqlite3.connect('walmart_assortment.db')

# Push data to SQL
df_sales.to_sql('sales', conn, if_exists='replace', index=False)
df_products.to_sql('products', conn, if_exists='replace', index=False)
df_stores.to_sql('stores', conn, if_exists='replace', index=False)
df_plano.to_sql('planogram', conn, if_exists='replace', index=False)

print("Database 'walmart_assortment.db' created successfully!")
conn.close()

