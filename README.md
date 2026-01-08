# Modular Optimization Engine (MOE)

🚀 **Automated Assortment Activation & Space Planning Tool**

**Tech Stack:** Python (Pandas, NumPy), SQL, Generative AI (LLM Prompting), Matplotlib

**Domain Focus:** Retail Operations, Planogram Efficiency, Inventory Strategy

---

## 📖 Project Overview

### The Problem: The Disconnect Between Strategy and Execution

In retail assortment planning, a critical gap often exists between **Financial Strategy** (what merchants buy) and **Operational Execution** (the reality on the store shelf). High-performing items are frequently recommended for stores that lack the physical shelf capacity to accommodate them. This leads to failed implementations, frustrated store associates, and wasted labor hours.

### The Solution: The Modular Optimization Engine (MOE)

The **Modular Optimization Engine (MOE)** is a full-stack analytics tool designed to bridge this gap. It moves beyond simple sales metrics to calculate **Sales Per Linear Inch (SPLI)**, identifying space-inefficient SKUs.

Crucially, MOE uses a **Constraint-Based Logic Engine** to ensure that any recommended replacement physically fits the specific shelf gap (Width/Height) left by the deleted item. This guarantees 100% planogram compliance *before* the instruction ever reaches the store, ensuring that merchandising plans are not just financially sound, but operationally executable.

---

## 🛠 Key Features

### 1. Regional Market Clustering (Data Architecture)

*   **Concept:** Generated a robust synthetic dataset representing **20 stores** across a "Northwest Arkansas" market cluster.
*   **Logic:** Simulates real-world variables including Store Format (Supercenter vs. Neighborhood Market), Traffic Profiles (High vs. Low), and Regional Demographics (University vs. Rural).
*   **Tech:** Python `pandas` for relational data generation.

### 2. Constraint-Based Optimization (The "Gap Analysis")

*   **Concept:** Standard analysis looks for "Top Sellers." This engine looks for **"Top Sellers that Fit."**
*   **Logic:**
    1.  Identifies "Delete Candidates" based on the lowest *Sales Per Linear Inch*.
    2.  Calculates the physical "Void Dimensions" (e.g., a 15-inch gap).
    3.  Scans the master catalog for replacement candidates where:
        `Candidate_Width * Facings <= Gap_Width`
*   **Impact:** Eliminates "impossible" planograms that frustrate store associates and lead to "dead space" on the shelf. My code doesn't just look for "Good Products." It looks for **"Good Products that Fit."**

### 3. AI-Powered Stakeholder Communication

*   **Concept:** Automates the "Cross-Functional Coordination" required for successful assortment activation.
*   **Logic:** Uses LLM prompting to dynamically generate two distinct outputs based on the optimization results:
    *   **Merchant Pitch:** A financial justification email focusing on Margin Lift and SPLI.
    *   **Store Ops Card:** A simplified, step-by-step execution guide for the stocking associate.

### 4. Performance Monitoring Dashboard

*   **Concept:** Visualizes the projected financial impact of the activation.
*   **Tech:** `Matplotlib` and `Seaborn` charts showing "Before vs. After" revenue lift and Store Format efficiency heatmaps.

---

## 📊 Technical Deep Dive

### The "Senior Analyst" SQL Query

This project moves beyond basic aggregation, using Window Functions and complex Joins to normalize sales data against physical dimensions.

```sql
/* Calculating Sales Per Linear Inch (SPLI) */
SELECT
    p.product_name,
    pl.shelf_id,
    -- Total Width occupied on shelf
    (p.width_inches * pl.facings) AS total_linear_inches,
    -- The Senior Analyst Metric: Revenue per Inch of Shelf Space
    ROUND(SUM(s.revenue) / (p.width_inches * pl.facings), 2) AS revenue_per_inch
FROM products p
JOIN planogram pl ON p.sku_id = pl.sku_id
JOIN sales_history s ON p.sku_id = s.sku_id
GROUP BY p.product_name, pl.shelf_id;
```

---

## 🤖 AI-Powered Communication Examples

### Merchant Pitch (Strategic Insights)

```
SUBJECT: Assortment Optimization Proposal - Store 3000 (Bentonville Supercenter)

Hi Team,

Based on Q3 performance data, I recommend an immediate modular update for the Home category in Bentonville.

The Proposal:
We are currently allocating 15 inches of shelf space to 'Home Item 34 - CozyNest Pillow', which is yielding only $0.85 SPLI. This is performing 40% below category average.

The Solution:
I propose swapping this for 'Home Item 89 - GreenThumb Ceramic Planter'.
1. Fit Compliance: Matches the exact 15" gap (No shelf moves required).
2. Upside: Based on regional trends, we project a margin lift of 15%.

Please approve this swap by EOD Friday for execution next week.
```

### Store Ops Instructions (Training Materials)

```
[MODULAR UPDATE TASK CARD]
LOCATION: Home Department, Aisle 12, Section 4

1. REMOVE:
   [ ] 'Home Item 34 - CozyNest Pillow'
   -> Action: Pull all units and apply yellow 'Clearance' stickers. Move to Flex Aisle.

2. CLEAN:
   [ ] Wipe down the empty 15-inch shelf section.

3. SET:
   [ ] Place 'Home Item 89 - GreenThumb Ceramic Planter'
   -> Facings: 1 Row (Fits exactly).
   -> Alignment: Align left edge with shelf notch.

4. TAG:
   [ ] Print and set new shelf label (UPC ends in 89).
```

---

## 📈 Performance Monitoring Dashboard

Here are the projected results from the optimization engine:

**Figure 1: Projected Revenue Lift**
<img width="1000" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/29cf4a70-d31e-43aa-ac13-dbea6a373479" />


**Figure 2: Store Format Efficiency Heatmap**
<img width="800" height="600" alt="Figure_2" src="https://github.com/user-attachments/assets/306b86ab-4433-45ee-84a8-d8aa9b939afb" />


---

## 📂 Project Structure

```
modular_logic/
│
├── 🖼️ Figure_1.png
├── 🖼️ Figure_2.png
├── 📝 README.md
│
├── 📁 Background/
│   ├── 📄 Insights.txt
│   ├── 📄 Insights2.txt
│   ├── 📄 Insights3.txt
│   ├── 📄 insights4.txt
│   └── 📝 README.md
│
├── 📁 Code/
│   ├── 🐍 assortment_dashboard.py   # Generates Matplotlib visualizations
│   ├── 🐍 communication_agent.py    # Simulates AI-powered stakeholder comms
│   ├── 🐍 data_generation.py        # Creates the synthetic regional dataset
│   ├── 🐍 data_warehouse.py         # Loads CSVs into a SQLite database
│   ├── 🐍 logic_engine.py           # Calculates SPLI and finds optimal replacements
│   └── 🐍 sql_explorer.py           # Interactive shell for database queries
│
└── 📁 Data/
    ├── 📄 plano_regional.csv
    ├── 📄 products_regional.csv
    ├── 📄 sales_regional.csv
    ├── 📄 stores_regional.csv
    └── 📄 walmart_assortment.db
```

---

## 🚀 How to Run

### Prerequisites

*   Python 3.x
*   The following Python libraries:
    *   `pandas`
    *   `numpy`
    *   `matplotlib`
    *   `seaborn`

You can install these with pip:
```bash
pip install pandas numpy matplotlib seaborn
```

### Execution Order

The project is designed to be run in a specific sequence to simulate a real-world analytics pipeline.

**Step 1: Generate the Synthetic Data**

This script creates the CSV files that serve as the foundation for the project.

```bash
python Code/data_generation.py
```

**Step 2: Create the Data Warehouse**

This script loads the CSVs into a SQLite database.

```bash
python Code/data_warehouse.py
```

**Step 3: Run the Optimization Engine**

This script performs the core analysis, identifying the delete candidate and finding a suitable replacement.

```bash
python Code/logic_engine.py
```

**Step 4: Generate Stakeholder Communications**

This script simulates the AI-powered communication, generating the merchant pitch and store ops card.

```bash
python Code/communication_agent.py
```

**Step 5: Visualize the Results**

This script generates the dashboard visualizations.

```bash
python Code/assortment_dashboard.py
```

**(Optional) Step 6: Explore the Data**

This script provides an interactive shell for running SQL queries against the database.

```bash
python Code/sql_explorer.py
```

---

## 🏁 Conclusion

The Modular Optimization Engine is more than just an analytics tool; it's a demonstration of how to connect high-level financial strategy with on-the-ground operational reality. By focusing on "Sales Per Linear Inch" and incorporating physical constraints into the optimization algorithm, this project provides a blueprint for a more effective and efficient assortment planning process.

The use of AI to automate stakeholder communication further enhances the project's value, showcasing a forward-thinking approach to cross-functional collaboration. This tool is designed to empower retailers to make smarter, data-driven decisions that are both profitable and executable.

