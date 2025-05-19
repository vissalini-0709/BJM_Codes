# This code to select multiple Holdings file, remove calculation type = 0 and save the extract in one folder.
# The code will prompt to select folders to save the files.
# Output file name will be same as input file.

import pandas as pd
from tkinter import Tk
from tkinter import filedialog
import os

# Function to process the input file
def process_records(file_path, output_dir):
    # Read the CSV file into a DataFrame with specified dtypes or low_memory option
    df = pd.read_csv(file_path, dtype={'Column45': str, 'Column318': str})  # Specify dtypes

    # 1. Remove rows where Period Type is not equal to 'Balances' and Calculation Result Type is equal to 0
    filtered_df = df[(df['Period Type'] == 'Balances') | (df['Calculation Result Type'] != 0)]

    # Display the number of remaining records
    record_count = filtered_df.shape[0]
    print(f"Number of records after filtering Period Type not equal to Balances and Calculation Result Type = 0 for {os.path.basename(file_path)}: {record_count}")

    # Save the filtered DataFrame to a new CSV file
    save_filtered_file(file_path, filtered_df, output_dir)

# Function to save the filtered DataFrame to a new CSV file
def save_filtered_file(original_file_path, filtered_df, output_dir):
    # Get the base name of the original file
    base_name = os.path.basename(original_file_path)
    
    # Create the new file path by joining the output directory and the base name
    new_file_path = os.path.join(output_dir, base_name)
    
    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(new_file_path, index=False)
    
    print(f"Filtered records saved to: {new_file_path}")

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

# Function to prompt for the output directory
def prompt_output_directory():
    # Hide the root Tkinter window
    Tk().withdraw()  
    # Prompt for the output directory
    output_dir = filedialog.askdirectory(
        title="Select Output Directory"
    )
    return output_dir

# Main execution flow
if __name__ == "__main__":
    selected_file_paths = open_file_dialog()
    
    if selected_file_paths:  # Check if files were selected
        output_dir = prompt_output_directory()
        
        if output_dir:  # Check if an output directory was selected
            for file_path in selected_file_paths:
                process_records(file_path, output_dir)
        else:
            print("No output directory was selected.")
    else:
        print("No files were selected.")
