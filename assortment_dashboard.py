import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==========================================
# 1. SETUP: SIMULATE THE "BEFORE & AFTER" DATA
# ==========================================
# In a real dashboard, this comes from the Phase 2 Output. 
# We manually create the dataframe here for the visual demo.

impact_data = {
    'Metric': ['Weekly Revenue', 'Weekly Margin', 'Sales Per Linear Inch'],
    'Old Assortment (Item 34)': [125.00, 35.00, 0.85], # The "Dog" we deleted
    'New Assortment (Item 89)': [210.00, 95.00, 1.45]  # The "Star" we added
}

df_impact = pd.DataFrame(impact_data)

# ==========================================
# 2. VISUALIZATION 1: THE IMPACT ASSESSMENT (Bar Chart)
# ==========================================
def plot_impact_chart():
    # Set the style
    sns.set_theme(style="whitegrid")
    
    # Reshape for plotting
    df_melted = df_impact.melt(id_vars="Metric", var_name="Scenario", value_name="Value")
    
    plt.figure(figsize=(10, 6))
    
    # Create Bar Chart
    chart = sns.barplot(
        data=df_melted, 
        x="Metric", 
        y="Value", 
        hue="Scenario", 
        palette=["#e74c3c", "#27ae60"] # Red for Old, Green for New
    )
    
    # Add Title and Labels
    plt.title('Projected Impact: Modular Optimization (Store 3000)', fontsize=16, fontweight='bold')
    plt.ylabel('Value ($)', fontsize=12)
    plt.xlabel('')
    
    # Add value labels on bars
    for container in chart.containers:
        chart.bar_label(container, fmt='$%.2f', padding=3)
        
    plt.tight_layout()
    plt.show()

# ==========================================
# 3. VISUALIZATION 2: THE OPPORTUNITY HEATMAP
# ==========================================
def plot_market_heatmap():
    # This visual answers: "Which stores have the biggest 'Space Efficiency' problem?"
    
    # Mock aggregated data: Category Efficiency (Sales per Inch) by Store Format
    heatmap_data = pd.DataFrame({
        'Supercenter': [1.8, 2.1, 1.2, 0.9],
        'Neighborhood Mkt': [1.4, 1.5, 0.8, 0.6],
        'Express': [2.5, 1.9, 0.5, 0.4]
    }, index=['Electronics', 'Personal Care', 'Home', 'Toys']) # Categories
    
    plt.figure(figsize=(8, 6))
    
    # Create Heatmap
    sns.heatmap(
        heatmap_data, 
        annot=True, 
        cmap="RdYlGn", # Red (Bad) to Green (Good)
        fmt=".1f", 
        linewidths=.5
    )
    
    plt.title('Efficiency Audit: Sales Per Linear Inch ($) by Format', fontsize=14, fontweight='bold')
    plt.ylabel('Category')
    plt.xlabel('Store Format')
    
    plt.tight_layout()
    plt.show()

# Run the functions
print("Generating Impact Charts...")
plot_impact_chart()
print("Generating Market Heatmap...")
plot_market_heatmap()