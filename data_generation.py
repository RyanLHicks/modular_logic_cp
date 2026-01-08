import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ==========================================
# CONFIGURATION
# ==========================================
NUM_PRODUCTS = 1000  # Large assortment
NUM_STORES = 20      # A full market cluster
DAYS_HISTORY = 90
START_DATE = datetime(2024, 6, 1)

# ==========================================
# 1. GENERATE REGIONAL STORE MASTER
# ==========================================
# We create a specific "Northwest Market" cluster
locations = [
    # Flagship / High Volume
    {'city': 'Bentonville', 'type': 'Supercenter', 'traffic': 'High', 'sq_ft': 180000},
    {'city': 'Rogers', 'type': 'Supercenter', 'traffic': 'High', 'sq_ft': 175000},
    {'city': 'Fayetteville', 'type': 'Supercenter', 'traffic': 'High', 'sq_ft': 185000},
    {'city': 'Springdale', 'type': 'Supercenter', 'traffic': 'Med', 'sq_ft': 160000},
    
    # Suburban / Commuter
    {'city': 'Centerton', 'type': 'Neighborhood Mkt', 'traffic': 'Med', 'sq_ft': 45000},
    {'city': 'Bella Vista', 'type': 'Supercenter', 'traffic': 'Med', 'sq_ft': 150000},
    {'city': 'Lowell', 'type': 'Neighborhood Mkt', 'traffic': 'Med', 'sq_ft': 42000},
    {'city': 'Farmington', 'type': 'Neighborhood Mkt', 'traffic': 'Med', 'sq_ft': 40000},
    
    # Rural / Outlying
    {'city': 'Pea Ridge', 'type': 'Neighborhood Mkt', 'traffic': 'Low', 'sq_ft': 38000},
    {'city': 'Gravette', 'type': 'Supercenter', 'traffic': 'Low', 'sq_ft': 120000},
    {'city': 'Siloam Springs', 'type': 'Supercenter', 'traffic': 'Med', 'sq_ft': 140000},
    {'city': 'Huntsville', 'type': 'Supercenter', 'traffic': 'Low', 'sq_ft': 110000},
    
    # Urban / Student (University Area)
    {'city': 'Fayetteville (campus)', 'type': 'Express', 'traffic': 'High', 'sq_ft': 15000},
    {'city': 'Fayetteville (MLK)', 'type': 'Supercenter', 'traffic': 'High', 'sq_ft': 170000},
]

# Expand to 20 stores by duplicating some types
while len(locations) < NUM_STORES:
    locations.append(random.choice(locations))

stores = []
for i, loc in enumerate(locations):
    # Calculate shelf space based on store size (approx 10% of sq_ft is shelf linear feet for our mockup)
    shelf_cap = int(loc['sq_ft'] * 0.005) 
    
    stores.append({
        'store_id': 3000 + i,
        'store_name': f"Store {3000+i} - {loc['city']} {loc['type']}",
        'city': loc['city'],
        'format': loc['type'],
        'traffic_profile': loc['traffic'],
        'shelf_capacity_ft': shelf_cap
    })

df_stores = pd.DataFrame(stores)

# ==========================================
# 2. GENERATE PRODUCT MASTER (Using previous Logic)
# ==========================================
# (Using the same category logic as before, just scaling it)
categories = {
    'Electronics': {'brands': ['TechNova', 'SoundWave'], 'types': ['4K TV', 'Headphones', 'Cable'], 'margin': (0.15, 0.25)},
    'Home': {'brands': ['CozyNest', 'GreenThumb'], 'types': ['Pillow', 'Bin', 'Planter'], 'margin': (0.40, 0.60)},
    'Toys': {'brands': ['FunZone', 'BrickBuilder'], 'types': ['Action Fig', 'Blocks', 'Doll'], 'margin': (0.35, 0.50)},
    'Personal Care': {'brands': ['GlowUp', 'PureSmile'], 'types': ['Shampoo', 'Soap', 'Lotion'], 'margin': (0.25, 0.45)},
    'Grocery': {'brands': ['GreatValue', 'TastyBite'], 'types': ['Cereal', 'Pasta', 'Coffee'], 'margin': (0.20, 0.35)}
}

products = []
for i in range(1, NUM_PRODUCTS + 1):
    cat_name = random.choice(list(categories.keys()))
    cat_data = categories[cat_name]
    
    # Simple constraints for size
    if cat_name == 'Electronics' and 'TV' in cat_data['types']:
        width, height = 40.0, 25.0
    elif cat_name == 'Home':
        width, height = 15.0, 15.0
    elif cat_name == 'Grocery' or cat_name == 'Personal Care':
        width, height = 3.0, 8.0
    else:
        width, height = 8.0, 10.0
        
    cost = round(random.uniform(5, 50), 2)
    price = round(cost * 1.4, 2)
    
    products.append({
        'sku_id': 50000 + i,
        'product_name': f"{cat_name} Item {i}",
        'category': cat_name,
        'width_inches': width,
        'height_inches': height,
        'unit_price': price,
        'unit_cost': cost
    })

df_products = pd.DataFrame(products)

# ==========================================
# 3. GENERATE PLANOGRAMS (Regional Logic)
# ==========================================
plano_data = []

for _, store in df_stores.iterrows():
    # Store-Specific Assortment Logic
    # 1. "University" stores sell more Electronics/Personal Care, less Home/Garden
    # 2. "Rural" stores sell more Home/Garden/Grocery
    
    store_cat_weights = [0.2, 0.2, 0.2, 0.2, 0.2] # Default
    if 'campus' in store['store_name']:
        store_cat_weights = [0.30, 0.05, 0.10, 0.35, 0.20] # High Elec/Personal
    elif 'Rural' in store['traffic_profile']:
        store_cat_weights = [0.10, 0.30, 0.15, 0.15, 0.30] # High Home/Grocery

    # Create weighted list of products specifically for this store
    # (Simplified for script length: we just pick random subset based on capacity)
    
    capacity_inches = store['shelf_capacity_ft'] * 12
    current_fill = 0
    shelf_num = 1
    
    shuffled_prods = df_products.sample(frac=1).reset_index(drop=True)
    
    for _, prod in shuffled_prods.iterrows():
        if current_fill >= capacity_inches: break
        
        facings = 1
        if 'High' in store['traffic_profile'] and prod['category'] == 'Grocery':
            facings = 2 # High traffic stores double face grocery
            
        plano_data.append({
            'store_id': store['store_id'],
            'shelf_id': shelf_num,
            'sku_id': prod['sku_id'],
            'facings': facings
        })
        current_fill += (prod['width_inches'] * facings)
        if current_fill % 48 < (prod['width_inches'] * facings): shelf_num += 1

df_plano = pd.DataFrame(plano_data)

# ==========================================
# 4. GENERATE SALES (Regional Traffic Logic)
# ==========================================
sales_data = []
dates = [START_DATE + timedelta(days=x) for x in range(DAYS_HISTORY)]

print("Generating Regional Sales Data...")

for date in dates:
    is_weekend = date.weekday() >= 5
    
    # Filter for active items only to speed up processing
    # (In a real DB we would join, here we loop carefully)
    
    # We simulate bulk sales to save processing time for 20 stores
    # Instead of iterating every product every day, we iterate Store-Planograms
    
    for _, row in df_plano.iterrows():
        # Random sampling: Not every item sells every day
        if random.random() > 0.10: continue 

        store_traffic = df_stores.loc[df_stores['store_id'] == row['store_id'], 'traffic_profile'].values[0]
        
        # Traffic Multiplier
        traffic_mult = 1.0
        if store_traffic == 'High': traffic_mult = 2.5
        elif store_traffic == 'Low': traffic_mult = 0.6
        
        # Weekend Multiplier
        weekend_mult = 1.5 if is_weekend else 1.0
        
        units = int(np.random.poisson(2) * traffic_mult * weekend_mult)
        
        if units > 0:
            prod_info = df_products[df_products['sku_id'] == row['sku_id']].iloc[0]
            sales_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'store_id': row['store_id'],
                'sku_id': row['sku_id'],
                'units_sold': units,
                'revenue': round(units * prod_info['unit_price'], 2),
                'margin': round(units * (prod_info['unit_price'] - prod_info['unit_cost']), 2)
            })

df_sales = pd.DataFrame(sales_data)

# Export
df_stores.to_csv('stores_regional.csv', index=False)
df_products.to_csv('products_regional.csv', index=False)
df_plano.to_csv('plano_regional.csv', index=False)
df_sales.to_csv('sales_regional.csv', index=False)

print(f"Regional Data Complete. {len(df_stores)} Stores, {len(df_sales)} Sales Records.")