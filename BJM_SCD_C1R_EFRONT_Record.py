import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import traceback

# ----------- Constants and Patterns -----------
BATCHES = {
    "SCD 12PM": [
        "SCD_EGA_SECURITYMASTER",
        "SCD_EGA_FX_Rates",
        "SCD_EGA_Security_Rating",
        "SCD_EGA_Capital_Info",
        "SCD_EGA_Transactions_PL",
        "SCD_EGA_Transactions_Costs",
        "SCD_EGA_Holdings",
        "SCD_EGA_GL_Balances",
        "SCD_EGA_NAV",
        "SCD_EGA_SAA_TAA"
    ],
    "SCD 5PM": [
        "SCD_EGA_SECURITYMASTER",
        "SCD_EGA_FX_Rates",
        "SCD_EGA_Security_Rating",
        "SCD_EGA_Capital_Info",
        "SCD_EGA_Transactions_PL",
        "SCD_EGA_Transactions_Costs",
        "SCD_EGA_Holdings",
        "SCD_EGA_GL_Balances",
        "SCD_EGA_NAV",
        "SCD_EGA_SAA_TAA"
    ],
    "C1R 5PM": [
        "C1R_TO_IDW_EQ_",
        "C1R_TO_IDW_FI_DOMESTIC_CORPORATE_BOND",
        "C1R_TO_IDW_FI_SUPRA",
        "C1R_TO_IDW_FI_GLOBAL_CORPORATE_BOND"
    ],
    "Efront 8PM": [
        "EFI_EGA_SECMAS",
        "EFI_EGA_TRX",
        "EFI_EGA_VALPOS"
    ],
    "SCD 12AM": [
        "SCD_EGA_SECURITYMASTER",
        "SCD_EGA_FX_Rates",
        "SCD_EGA_Security_Rating",
        "SCD_EGA_Capital_Info",
        "SCD_EGA_Transactions_PL",
        "SCD_EGA_Transactions_Costs",
        "SCD_EGA_Holdings",
        "SCD_EGA_GL_Balances",
        "SCD_EGA_NAV",
        "SCD_EGA_SAA_TAA"
    ]
}

SPECIAL_PATTERNS = {
    "C1R_TO_IDW_EQ_": "17:30:00",
    "C1R_TO_IDW_FI_DOMESTIC_CORPORATE_BOND": "17:30:00"
}

EXTRACT_PATTERNS = [
    "C1R_TO_IDW_FI_SUPRA",
    "C1R_TO_IDW_FI_GLOBAL_CORPORATE_BOND"
]

ADDITIONAL_TIMESTAMPS = {
    "EFI_EGA_SECMAS": "20:15:00",
    "EFI_EGA_TRX": "20:30:00",
    "EFI_EGA_VALPOS": "20:40:00"
}

REQUIRED_COLUMNS = {
    "SCD_EGA_FX_Rates": ['Base Currency', 'Price Currency', 'External Data Source'],
    "SCD_EGA_Security_Rating": ['Instrument Type', 'Rating', 'Long Term Outlook'],
    "SCD_EGA_Transactions_PL": ['Current Version'],
    "SCD_EGA_Holdings": ['Period Type', 'Calculation Result Type']
}

# ----------- Helper Functions -----------

def matches_pattern(filename, pattern):
    """Case-insensitive check if filename starts with or contains pattern"""
    fn_lower = filename.lower()
    pattern_lower = pattern.lower()
    return fn_lower.startswith(pattern_lower) or (pattern_lower in fn_lower)

def extract_timestamps(file_paths):
    """Extract timestamps based on file patterns."""
    timestamps = {}
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        for pattern in SPECIAL_PATTERNS:
            if pattern in filename:
                timestamps[filename] = SPECIAL_PATTERNS[pattern]
                break
        else:
            for pattern in ADDITIONAL_TIMESTAMPS:
                if pattern in filename:
                    timestamps[filename] = ADDITIONAL_TIMESTAMPS[pattern]
                    break
            else:
                for extract_pattern in EXTRACT_PATTERNS:
                    if extract_pattern in filename:
                        match = re.search(r'(\d{6})\.', filename)
                        if match:
                            timestamp = match.group(1)
                            formatted_timestamp = f"{timestamp[:2]}:{timestamp[2:4]}:{timestamp[4:]}"
                            timestamps[filename] = formatted_timestamp
                        break
                else:
                    for patterns in BATCHES.values():
                        for pattern in patterns:
                            if pattern in filename:
                                match = re.search(r'(\d{6})\.', filename)
                                if match:
                                    timestamp = match.group(1)
                                    formatted_timestamp = f"{timestamp[:2]}:{timestamp[2:4]}:{timestamp[4:]}"
                                    timestamps[filename] = formatted_timestamp
                                break
                        if filename in timestamps:
                            break
    return timestamps

def filter_and_count_data(file_paths, patterns):
    """Filter files based on patterns and count data rows."""
    results = []
    for pattern in patterns:
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            if matches_pattern(filename, pattern):
                try:
                    df = pd.read_csv(file_path, low_memory=False)
                    record_count = len(df)
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
                    record_count = 0
                results.append((filename, record_count, pattern))
                break
    return results

def process_file(file_path, patterns):
    """Process a single file based on defined logic."""
    filename = os.path.basename(file_path)
    result = {'pattern': None, 'filename': filename, 'errors': [], 'number': None}
    try:
        df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
    except Exception as e:
        result['results'].append(f"CSV Read Error: {str(e)}")
        return result

    for pattern in patterns:
        if matches_pattern(filename, pattern):
            result['pattern'] = pattern
            break

    if not result['pattern']:
        result['results'].append("No matching file pattern found")
        return result

    required = REQUIRED_COLUMNS.get(result['pattern'], [])
    missing = [col for col in required if col not in df.columns]
    if missing:
        result['results'].append(f"Missing columns: {', '.join(missing)}")
        return result

    try:
        if result['pattern'] == "SCD_EGA_SECURITYMASTER":
            result['number'] = len(df)
        elif result['pattern'] == "SCD_EGA_FX_Rates":
            deduped = df.drop_duplicates(subset=REQUIRED_COLUMNS['SCD_EGA_FX_Rates'], keep='first')
            result['number'] = len(deduped)
        elif result['pattern'] == "SCD_EGA_Security_Rating":
            df = df[df['Instrument Type'] != 'Right']
            df = df[~((df['Instrument Type'] == 'Bond') & (df['Rating'] == 'N/S'))]
            bond = df[df['Instrument Type'] == 'Bond']
            result['number'] = len(bond)
        elif result['pattern'] == "SCD_EGA_Capital_Info":
            result['number'] = len(df)
        elif result['pattern'] == "SCD_EGA_Transactions_PL":
            if 'Current Version' in df.columns:
                counts = df['Current Version'].value_counts()
                result['number'] = counts.get('Yes', 0)
        elif result['pattern'] == "SCD_EGA_Transactions_Costs":
            result['number'] = len(df) * 2
        elif result['pattern'] == "SCD_EGA_Holdings":
            balances = df[df['Period Type'] == 'Balances']
            others = df[(df['Period Type'] != 'Balances') & (df['Calculation Result Type'] != 0)]
            result['number'] = len(balances) + len(others)
        elif result['pattern'] in ["SCD_EGA_GL_Balances", "SCD_EGA_NAV", "SCD_EGA_SAA_TAA"]:
            result['number'] = len(df)
        else:
            result['number'] = len(df)
    except Exception as e:
        result['results'].append(f"Processing Error: {str(e)}")

    return result

# ----------- Main Workflow -----------

def run_batch(batch_name, folder_path, patterns):
    """Process all files in a folder for a given batch."""
    all_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".csv"):
                all_files.append(os.path.join(root, file))

    timestamps = extract_timestamps(all_files)
    counts = filter_and_count_data(all_files, patterns)
    processed_files = [process_file(f, patterns) for f in all_files]

    results = []
    for filename, record_count, pattern in counts:
        processed_result = next((p for p in processed_files if p['filename'] == filename), None)
        errors = processed_result['results'] if processed_result and 'results' in processed_result else []
        number = processed_result['number'] if processed_result and 'number' in processed_result else None

        row = {
            "Batch": batch_name,
            "Filename": filename,
            "Pattern": pattern,
            "Timestamp": timestamps.get(filename, ""),
            "Raw Records": record_count,
            "Pre_processed Records": number,
            "Errors": "; ".join(errors)
        }
        results.append(row)
    return results

def main():
    root = tk.Tk()
    root.withdraw()
    all_results = []

    # Process each batch
    for batch, patterns in BATCHES.items():
        messagebox.showinfo("Folder Selection", f"Select folder for {batch}")
        folder_path = filedialog.askdirectory(title=f"Select folder for {batch}")
        if not folder_path:
            messagebox.showinfo("Skipped", f"No folder selected for {batch}. Skipping.")
            continue

        batch_results = run_batch(batch, folder_path, patterns)
        all_results.extend(batch_results)

    # Display results in terminal table
    if all_results:
        headers = ["Batch", "Filename", "Pattern", "Timestamp", "Raw Records", "Pre_processed Records", "Errors"]
        try:
            print(tabulate(all_results, headers="keys", tablefmt="grid"))
        except Exception as e:
            print(f"Error displaying table: {e}")

        # Export to Excel
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        main_folder = os.path.dirname(folder_path)  # Use the directory of the last processed batch
        output_file = os.path.join(main_folder, f"BatchJobDetails_{timestamp}.xlsx")
        try:
            df = pd.DataFrame(all_results)
            df.to_excel(output_file, index=False)
            print(f"\nResults exported to: {output_file}")
            messagebox.showinfo("Success", f"Results exported to:\n{output_file}")
        except Exception as e:
            print(f"Error exporting to Excel: {e}")

    else:
        print("No files processed.")

if __name__ == "__main__":
    main()
