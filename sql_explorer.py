import sqlite3
import pandas as pd

def run_shell():
    db_path = 'walmart_assortment.db'
    conn = sqlite3.connect(db_path)
    
    print("="*60)
    print("🛒 WALMART ASSORTMENT DATA SHELL")
    print("Type your SQL query below. Type 'exit' to quit.")
    print("="*60)
    
    while True:
        print("\nSQL > ", end="")
        query = input()
        
        if query.lower() in ['exit', 'quit']:
            break
            
        try:
            # We use pandas to make the output look like a nice Excel table
            df = pd.read_sql(query, conn)
            if df.empty:
                print("✅ Query executed successfully, but returned no results.")
            else:
                print(f"\n--- Result ({len(df)} rows) ---")
                print(df.to_string(index=False)) # Prints a pretty table
                
        except Exception as e:
            print(f"❌ Error: {e}")

    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    run_shell()