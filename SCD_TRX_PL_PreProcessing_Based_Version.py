#this code will display total number of trx pl record after remove current version = 0 values

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

# Hide the main tkinter window
Tk().withdraw()

# Prompt user to select multiple CSV files
file_paths = askopenfilenames(title="Select CSV files", filetypes=[("CSV files", "*.csv")])

# Check if any files were selected
if not file_paths:
    print("No files selected.")
    exit()

# Loop through each selected file
for file_path in file_paths:
    print(f"\nProcessing file: {file_path}")
    
    # Read the CSV file with low_memory=False
    try:
        df = pd.read_csv(file_path, low_memory=False)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        continue

    # Check if "Current version" column exists
    if "Current Version" not in df.columns:
        print(f"Error: 'Current version' column not found in {file_path}. Skipping...")
        continue

    # Clean the "Current version" column by stripping leading/trailing spaces
    df['Current Version'] = df['Current Version'].astype(str).str.strip()

    # Count records based on "Current version" column
    current_version_yes = df[df["Current Version"] == "Yes"].shape[0]
    current_version_no = df[df["Current Version"] == "No"].shape[0]

    # Display results
    print(f"Current Version = Yes : Total number of records: {current_version_yes}")
    print(f"Current Version = No : Total number of records: {current_version_no}")

    # Optional: Check if there are any other values in the "Current version" column
    other_values = df[~df["Current Version"].isin(["Yes", "No"])]
    if not other_values.empty:
        print(f"Other values in 'Current version' column: {other_values['Current version'].unique()}")
