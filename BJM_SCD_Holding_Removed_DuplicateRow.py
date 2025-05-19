#21stApril
#this code allow to select multiple files and removed duplicate records.
#"Portfolio",
#"Portfolio Name",
#"Valuation Date",
#"Security ID",
#"Portfolio (IK)",
#"Security (IK)",
#"Holding (IK)",
#"Model Portfolio (IK)",
#"Calculation Result Type",
#"Underlying Security (IK)",
#"Portfolio Calculation"

import os
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

def process_file(file_path):
    # Read all columns as string to preserve formatting exactly
    df = pd.read_csv(file_path, dtype=str)
    
    original_columns = df.columns.tolist()
    
    # Create a temporary datetime column for Calculation Date parsing (for comparison only)
    df['_Calculation_Date_dt'] = pd.to_datetime(df['Calculation Date'], errors='coerce')
    
    key_columns = [
        "Portfolio",
        "Portfolio Name",
        "Valuation Date",
        "Security ID",
        "Portfolio (IK)",
        "Security (IK)",
        "Holding (IK)",
        "Model Portfolio (IK)",
        "Calculation Result Type",
        "Underlying Security (IK)",
        "Portfolio Calculation"
    ]
    
    # Find duplicates based on key columns (excluding Calculation Date)
    duplicates = df[df.duplicated(subset=key_columns, keep=False)]
    
    if duplicates.empty:
        print(f"No duplicates found in: {os.path.basename(file_path)}")
        return
    
    # For each duplicate group, get index of row with latest Calculation Date (using temporary datetime column)
    latest_idx = duplicates.groupby(key_columns)['_Calculation_Date_dt'].idxmax()
    latest_entries = duplicates.loc[latest_idx]
    
    # Remove all duplicates from original
    non_duplicates = df.drop(duplicates.index)
    
    # Append latest entries back
    final_output = pd.concat([non_duplicates, latest_entries])
    
    # Drop the temporary datetime column before saving
    final_output = final_output.drop(columns=['_Calculation_Date_dt'])
    duplicates = duplicates.drop(columns=['_Calculation_Date_dt'])
    
    base_folder = os.path.dirname(file_path)
    latest_folder = os.path.join(base_folder, "Keep Latest Calculation Date")
    dup_folder = os.path.join(base_folder, "Duplicated Records")
    
    os.makedirs(latest_folder, exist_ok=True)
    os.makedirs(dup_folder, exist_ok=True)
    
    filename = os.path.basename(file_path)
    
    # Save cleaned file with original columns order and no index
    final_output.to_csv(os.path.join(latest_folder, filename), columns=original_columns, index=False)
    
    # Save duplicates file with "Duplicate_" prefix and original columns order
    dup_filename = f"Duplicate_{filename}"
    duplicates.to_csv(os.path.join(dup_folder, dup_filename), columns=original_columns, index=False)
    
    print(f"Processed: {filename}")
    print(f"  - Cleaned file saved to: {latest_folder}")
    print(f"  - Duplicates saved to: {dup_folder} as {dup_filename}\n")

def main():
    Tk().withdraw()
    files = askopenfilenames(title="Select CSV File(s)", filetypes=[("CSV Files", "*.csv")])
    
    if not files:
        print("No files selected.")
        return
    
    for f in files:
        process_file(f)

if __name__ == "__main__":
    main()
