#1. Remove Instrument Type = Right
#2. Remove Instrument Type = Bond and Rating = N/S
#3. Display number  Instrument Type = Equity
#4. Display number of Instrument Type = Bond
#5. Display Instrument Type = Bond and Long Term Outlook not equal to NA
#6. Display (BOND + Long Term Outlook not equal to NA)

import pandas as pd
from tkinter import Tk
from tkinter import filedialog

# Function to process the input file
def process_instruments(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # 1. Remove Instrument Type = Right
    df = df[df['Instrument Type'] != 'Right']

    # 2. Remove Instrument Type = Bond and Rating = N/S
    df = df[~((df['Instrument Type'] == 'Bond') & (df['Rating'] == 'N/S'))]

    # 3. Display number of Instrument Type = Equity
    equity_count = df[df['Instrument Type'] == 'Equity'].shape[0]
    print(f"Number of Instrument Type = Equity: {equity_count}")

    # 4. Display number of Instrument Type = Bond
    bond_count = df[df['Instrument Type'] == 'Bond'].shape[0]
    print(f"Number of Instrument Type = Bond: {bond_count}")

    # 5. Display Instrument Type = Bond and Long Term Outlook not equal to NA
    bond_long_term_outlook_count = df[(df['Instrument Type'] == 'Bond') & (df['Long Term Outlook'].notna())].shape[0]
    print(f"Number of Bond with Long Term Outlook not equal to NA: {bond_long_term_outlook_count}")

    # 6. Display point 4 + point 5
    total_bond_count = bond_count + bond_long_term_outlook_count
    print(f"Total Bonds (BOND + Long Term Outlook not equal to NA): {total_bond_count}")

# Function to open a file dialog and select a CSV file
def open_file_dialog():
    # Hide the root Tkinter window
    Tk().withdraw()  
    # Open a file dialog and return the selected file path
    file_path = filedialog.askopenfilename(
        title="Select a CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    return file_path

# Main execution flow
if __name__ == "__main__":
    selected_file_path = open_file_dialog()
    
    if selected_file_path:  # Check if a file was selected
        process_instruments(selected_file_path)
    else:
        print("No file was selected.")
