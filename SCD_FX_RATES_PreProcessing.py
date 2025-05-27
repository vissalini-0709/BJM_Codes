#this code will meger all the same External Data Source, Base Currency and Price Curreny in FX Rate file
# Will export the merged file and the result will show total number of record available.

import pandas as pd
from tkinter import Tk
from tkinter import filedialog
import os

def select_file():
    """Prompt user to select a file."""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("CSV Files", ".csv")])
    return file_path

def save_file(file_name):
    """Prompt user to save a file."""
    root = Tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(title="Save Output File", defaultextension=".csv", initialfile=file_name)
    return save_path

def merge_rows(df):
    """Merge rows based on conditions and remove duplicates."""
    # Group by 'Base Currency', 'Price Currency', 'External Data Source'
    # and aggregate other columns by concatenating values
    grouped_df = df.groupby(['Base Currency', 'Price Currency', 'External Data Source']).agg(lambda x: ', '.join(map(str, x))).reset_index()
    
    # Remove duplicate columns
    grouped_df = grouped_df.T.drop_duplicates().T
    
    return grouped_df

def main():
    # Select input file
    input_file_path = select_file()
    
    if not input_file_path:
        print("No file selected.")
        return
    
    # Load input file
    try:
        df = pd.read_csv(input_file_path)
    except Exception as e:
        print(f"Failed to load file: {e}")
        return
    
    # Check if required columns exist
    required_columns = ['Base Currency', 'Price Currency', 'External Data Source']
    if not all(col in df.columns for col in required_columns):
        print("The file does not contain all required columns.")
        return
    
    # Display total number of input records
    print(f"Total input records: {len(df)}")
    
    # Merge rows
    merged_df = merge_rows(df)
    
    # Display total number of output records
    print(f"Total output records after merging: {len(merged_df)}")
    
    # Generate output file name
    base_name, extension = os.path.splitext(input_file_path)
    output_file_name = f"{base_name}_1.csv"
    i = 1
    while os.path.exists(output_file_name):
        i += 1
        output_file_name = f"{base_name}_{i}.csv"
    
    # Prompt to save output file
    save_path = save_file(output_file_name)
    
    if not save_path:
        print("No save path selected.")
        return
    
    # Save output file
    try:
        merged_df.to_csv(save_path, index=False)
        print(f"File saved successfully as {save_path}")
    except Exception as e:
        print(f"Failed to save file: {e}")

if __name__ == "__main__":
    main()
