import pandas as pd

# ==========================================
# 1. LOAD THE REGIONAL DATA
# ==========================================
df_sales = pd.read_csv('sales_regional.csv')
df_plano = pd.read_csv('plano_regional.csv')
df_products = pd.read_csv('products_regional.csv')
df_stores = pd.read_csv('stores_regional.csv')

# ==========================================
# 2. CALCULATE "SALES PER LINEAR INCH" (The Metric)
# ==========================================
# We need to know how valuable each inch of shelf space is.

# Aggregated Sales by Store/SKU
store_sales = df_sales.groupby(['store_id', 'sku_id'])['revenue'].sum().reset_index()

# Merge with Planogram to get Facings
performance_data = pd.merge(df_plano, store_sales, on=['store_id', 'sku_id'], how='left')
performance_data['revenue'] = performance_data['revenue'].fillna(0) # Handle 0 sales items

# Merge with Products to get Dimensions
performance_data = pd.merge(performance_data, df_products, on='sku_id', how='left')

# CALCULATE EFFICIENCY METRICS
# Total Width Used = Product Width * Facings
performance_data['total_linear_width'] = performance_data['width_inches'] * performance_data['facings']
# Sales Per Linear Inch (SPLI)
performance_data['SPLI'] = performance_data['revenue'] / performance_data['total_linear_width']

# ==========================================
# 3. IDENTIFY THE "DELETE CANDIDATE"
# ==========================================
# Let's focus on Store 3000 (Bentonville Supercenter) for this analysis
target_store = 3000
store_data = performance_data[performance_data['store_id'] == target_store].copy()

# Sort by SPLI (Low to High) to find the worst performers
worst_performer = store_data.sort_values(by='SPLI').iloc[0]

print(f"--- DELETE RECOMMENDATION ---")
print(f"Store: {target_store}")
print(f"Delete Candidate: {worst_performer['product_name']}")
print(f"Reason: Lowest Sales Per Linear Inch (${round(worst_performer['SPLI'], 2)})")
print(f"Gap Created: {worst_performer['total_linear_width']} inches")
print(f"Category: {worst_performer['category']}")
print("-" * 30)

# ==========================================
# 4. THE OPTIMIZATION ENGINE (Find the Replacement)
# ==========================================
# LOGIC: 
# 1. Must be same Category.
# 2. Must fit in the Gap (New_Width * Facings <= Gap_Width).
# 3. Must NOT already be in this store.

# Step A: Define the Constraint
gap_width = worst_performer['total_linear_width']
target_category = worst_performer['category']
existing_skus = store_data['sku_id'].unique()

# Step B: Filter the Master Catalog for Candidates
candidates = df_products[
    (df_products['category'] == target_category) &      # Same Category
    (~df_products['sku_id'].isin(existing_skus)) &      # Not currently in store
    (df_products['width_inches'] <= gap_width)          # FITS IN THE HOLE
].copy()

# Step C: Rank Candidates
# In a real scenario, we'd use "Market Trend" data. 
# Here, we will use 'Unit Price' as a proxy for "Premium Up-sell Opportunity"
candidates = candidates.sort_values(by='unit_price', ascending=False)

if not candidates.empty:
    best_replacement = candidates.iloc[0]
    
    # Calculate fit
    facings_fit = int(gap_width // best_replacement['width_inches'])
    
    print(f"--- ADD RECOMMENDATION ---")
    print(f"Proposed Item: {best_replacement['product_name']}")
    print(f"Why: Top available item fitting the {gap_width}\" gap.")
    print(f"Item Width: {best_replacement['width_inches']}\"")
    print(f"Suggested Facings: {facings_fit}")
    print(f"New Linear Width: {best_replacement['width_inches'] * facings_fit}\"")
    print(f"Potential Revenue Upside: Higher price point item (${best_replacement['unit_price']})")
else:
    print("No valid replacement found that fits dimensions.")