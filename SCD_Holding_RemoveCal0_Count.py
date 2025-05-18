# This code to select multiple Holdings file, remove calculation type = 0 
# Save the output files at same path and add _1 at the end of the file name

import pandas as pd
from tkinter import Tk
from tkinter import filedialog
import os

# Function to process the input file
def process_records(file_path):
    # Read the CSV file into a DataFrame with specified dtypes or low_memory option
    df = pd.read_csv(file_path, dtype={'Column45': str, 'Column318': str})  # Specify dtypes

    # 1. Remove rows where Period Type is not equal to 'Balances' and Calculation Result Type is equal to 0
    filtered_df = df[(df['Period Type'] == 'Balances') | (df['Calculation Result Type'] != 0)]

    # Display the number of remaining records
    record_count = filtered_df.shape[0]
    print(f"Number of records after filtering Period Type not equal to Balances and Calculation Result Type = 0 for {os.path.basename(file_path)}: {record_count}")

    # Save the filtered DataFrame to a new CSV file
    save_filtered_file(file_path, filtered_df)

# Function to save the filtered DataFrame to a new CSV file
def save_filtered_file(original_file_path, filtered_df):
    # Create the new file name by modifying the original file name
    base_name, _ = os.path.splitext(original_file_path)
    new_file_name = f"{base_name}_1.csv"
    
    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(new_file_name, index=False)
    
    print(f"Filtered records saved to: {new_file_name}")

# Function to open a file dialog and select multiple CSV files
def open_file_dialog():
    # Hide the root Tkinter window
    Tk().withdraw()  
    # Open a file dialog and return the selected file paths
    file_paths = filedialog.askopenfilenames(
        title="Select CSV Files",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    return file_paths

# Main execution flow
if __name__ == "__main__":
    selected_file_paths = open_file_dialog()
    
    if selected_file_paths:  # Check if files were selected
        for file_path in selected_file_paths:
            process_records(file_path)
    else:
        print("No files were selected.")
