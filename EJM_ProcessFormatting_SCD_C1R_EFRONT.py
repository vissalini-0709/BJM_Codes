#Perfect Code for SCD,C1R and EFRONT
#This code will prompt to input EJM Processed record excel file, 
#Once inserted it will extract value based process name and stream.
#This code can be used if the Start Time and End Time at any column.

import pandas as pd
import re
import os
import collections
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from datetime import datetime

# --- Combine parent_patterns from both programs ---
parent_patterns = {
    # Program 1 patterns
    'inbnd_scd_smf': [
        (1, 'eagle_ml_2_0_default_in_xml_smf_generic_sec', 2, 'eagle_ml-2-0_default_in_xml_smf_generic', None, None)
    ],
    'inbnd_scd_fxrate': [
        (1, 'eagle_ml_2_0_default_in_xml_reference', 2, 'eagle_ml-2-0_default_in_xml_reference', None, None)
    ],
    'inbnd_scd_secrating': [
        (1, 'load_issuer_rating', 2, 'eagle_ml-2-0_default_in_xml_reference', None, None),
        (1, 'load_security_rating', 2, 'eagle_ml-2-0_default_in_xml_reference', None, None)
    ],
    'inbnd_scd_capinfo': [
        (1, 'eagle_ml_2_default_i_xml_reference', 2, 'eagle_ml-2-0_default_in_xml_reference', None, None)
    ],
    'inbnd_scd_txn': [
        (1, 'eagle_ml20_default_in_xml_warehouse_preproc_txn', 2, 'eagle_ml-2-0_default_in_xml_warehouse_preproc', None, None),
        (1, 'eagle_ml20_default_in_xml_warehouse_preproc_txn_fee', 2, 'eagle_ml-2-0_default_in_xml_warehouse_preproc', None, None)
    ],
    'inbnd_scd_holdings': [
        (1, 'inbnd_scd_holdings_positions', 2, 'inbnd_scd_holdings_positions_load', 3, 'eagle_default_eds_warehouse')
    ],
    'inbnd_scd_glbal': [
        (1, 'eagle_ml_2_0_default_in_xml_warehouse_preproc_gl_balances', 2, 'eagle_ml-2-0_default_in_xml_warehouse_preproc', None, None)
    ],
    'inbnd_scd_nav': [
        (1, 'eagle_ml_2_0_default_in_xml_warehouse_preproc_gl_balances', 2, 'eagle_ml-2-0_default_in_xml_warehouse_preproc', None, None)
    ],
    'inbnd_scd_saataa': [
        (1, 'inbnd_scd_saataa_uploader', 2, 'inbnd_scd_saataa_uploader', None, None)
    ],
    # Program 2 patterns
    'inbnd_factset_r_smf_fi': [
        (1, 'eagle_ml20_default_in_xml_reference', 2, 'eagle_ml-2-0_default_in_xml_reference', None, None)
    ],
    'inbnd_factset_r_smf_eq': [
        (1, 'eagle_ml20_default_in_xml_warehouse_preproc', 2, 'eagle_ml-2-0_default_in_xml_warehouse_preproc', None, None)
    ],
    'inbnd_efront_smf': [
        (1, 'eagle_ml20_default_in_xml_smf_generic', 2, 'eagle_ml-2-0_default_in_xml_smf_generic', None, None)
    ],
    'inbnd_efront_txn': [
        (1, 'eagle_ml_2_0_default_in_xml_warehouse_preproc', 2, 'eagle_ml-2-0_default_in_xml_warehouse_preproc', None, None)
    ],
    'inbnd_efront_holdings': [
        (1, 'inbnd_efront_holdings_load', 2, 'eagle_default_eds_warehouse', None, None)
    ]
}

def parse_successful_total(text):
    match = re.search(r'successful:\s*(\d+)\s+total:\s*(\d+)', str(text), re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def extract_date_time(date_time_val):
    if pd.isna(date_time_val):
        return '', ''
    try:
        dt = pd.to_datetime(date_time_val)
        return dt.strftime("%d/%m/%y"), dt.strftime("%H:%M:%S")
    except Exception:
        parts = str(date_time_val).split(' ')
        if len(parts) == 2:
            return parts[0], parts[1]
        return date_time_val, ''

def extract_time_only(date_time_val):
    if pd.isna(date_time_val):
        return ''
    try:
        dt = pd.to_datetime(date_time_val)
        return dt.strftime("%H:%M:%S")
    except Exception:
        parts = str(date_time_val).split(' ')
        if len(parts) == 2:
            return parts[1]
        return ''

def safe_iat(df, row_idx, col_idx):
    if (row_idx is None or col_idx is None or
        not isinstance(row_idx, int) or not isinstance(col_idx, int)):
        return None
    if row_idx < 0 or row_idx >= len(df):
        return None
    if col_idx < 0 or col_idx >= df.shape[1]:
        return None
    return df.iat[row_idx, col_idx]

def extract_holdings_values(df, parent_row):
    child_idx = None
    for c in range(parent_row + 1, len(df)):
        child_val = safe_iat(df, c, 1)
        if child_val and "inbnd_scd_holdings_positions" in str(child_val).lower():
            child_idx = c
            break
    if child_idx is None:
        return ("", 0, 0)

    grandchild_idx = None
    for g in range(child_idx + 1, len(df)):
        grandchild_val = safe_iat(df, g, 2)
        if grandchild_val and "inbnd_scd_holdings_positions_load" in str(grandchild_val).lower():
            grandchild_idx = g
            break
    if grandchild_idx is None:
        return ("", 0, 0)

    great_grandchild_idx = None
    for gg in range(grandchild_idx + 1, len(df)):
        great_grandchild_val = safe_iat(df, gg, 3)
        if great_grandchild_val and "eagle_default_eds_warehouse" in str(great_grandchild_val).lower():
            great_grandchild_idx = gg
            break

    if great_grandchild_idx is not None:
        val = safe_iat(df, great_grandchild_idx, 3)
    else:
        val = safe_iat(df, grandchild_idx, 2)

    x, y = parse_successful_total(val)
    if x is None or y is None:
        x, y = 0, 0

    stream_names = []
    if grandchild_idx is not None:
        stream_names.append(safe_iat(df, grandchild_idx, 2))
    return (', '.join(str(s) for s in stream_names if s), y, x)

def find_column_index(df, header_name):
    for idx, col in enumerate(df.columns):
        if str(col).strip().lower() == header_name.strip().lower():
            return idx
    return None

def process_file(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    df.columns = df.columns.str.strip()

    # Find Start Date and End Date columns dynamically
    start_date_col = find_column_index(df, "Start Date")
    end_date_col = find_column_index(df, "End Date")
    if start_date_col is None or end_date_col is None:
        raise ValueError("Could not find 'Start Date' or 'End Date' columns in the input file.")

    results = []

    for i in range(len(df)):
        parent_val = safe_iat(df, i, 0)
        if parent_val is None:
            continue
        parent = str(parent_val).strip()
        matched_parent_key = None
        for key in parent_patterns.keys():
            if key.lower() in parent.lower():
                matched_parent_key = key
                break

        if not matched_parent_key:
            continue

        # Extract dates/times using dynamic columns
        start_date_val = safe_iat(df, i, start_date_col)
        end_date_val = safe_iat(df, i, end_date_col)
        date_part, start_time = extract_date_time(start_date_val)
        end_time = extract_time_only(end_date_val)

        stream_names = []
        total_received = 0
        total_processed = 0

        found_any = False

        # Special handling for inbnd_scd_holdings (from Program 1)
        if matched_parent_key == 'inbnd_scd_holdings':
            stream_name_out, total_received, total_processed = extract_holdings_values(df, i)
            found_any = bool(stream_name_out)
        else:
            patterns = parent_patterns[matched_parent_key]
            for (child_col, child_substr, grandchild_col, grandchild_substr, great_grandchild_col, great_grandchild_substr) in patterns:
                child_idx = None
                for c in range(i + 1, len(df)):
                    next_parent_val = safe_iat(df, c, 0)
                    if next_parent_val is not None and any(k.lower() in str(next_parent_val).lower() for k in parent_patterns.keys()):
                        break
                    child_val = safe_iat(df, c, child_col)
                    if child_val is None:
                        continue
                    child_str = str(child_val).strip()
                    if child_substr.lower() in child_str.lower():
                        child_idx = c
                        break
                if child_idx is None:
                    continue

                grandchild_idx = None
                for g in range(child_idx + 1, len(df)):
                    next_parent_val = safe_iat(df, g, 0)
                    if next_parent_val is not None and any(k.lower() in str(next_parent_val).lower() for k in parent_patterns.keys()):
                        break
                    grandchild_val = safe_iat(df, g, grandchild_col)
                    if grandchild_val is None:
                        continue
                    grandchild_str = str(grandchild_val).strip()
                    if grandchild_substr.lower() in grandchild_str.lower() and re.search(r'successful:\s*\d+\s+total:\s*\d+', grandchild_str, re.IGNORECASE):
                        grandchild_idx = g
                        break

                great_grandchild_idx = None
                if great_grandchild_col is not None and great_grandchild_substr is not None and grandchild_idx is not None:
                    for gg in range(grandchild_idx + 1, len(df)):
                        next_parent_val = safe_iat(df, gg, 0)
                        if next_parent_val is not None and any(k.lower() in str(next_parent_val).lower() for k in parent_patterns.keys()):
                            break
                        great_grandchild_val = safe_iat(df, gg, great_grandchild_col)
                        if great_grandchild_val is None:
                            continue
                        great_grandchild_str = str(great_grandchild_val).strip()
                        if great_grandchild_substr.lower() in great_grandchild_str.lower() and re.search(r'successful:\s*\d+\s+total:\s*\d+', great_grandchild_str, re.IGNORECASE):
                            great_grandchild_idx = gg
                            break

                found_any = True
                if grandchild_idx is not None and grandchild_col is not None:
                    stream_names.append(safe_iat(df, grandchild_idx, grandchild_col))

                x, y = 0, 0
                if grandchild_idx is not None and grandchild_col is not None:
                    val = safe_iat(df, grandchild_idx, grandchild_col)
                    x, y = parse_successful_total(val)
                    if x is None or y is None:
                        x, y = 0, 0
                if great_grandchild_idx is not None and great_grandchild_col is not None:
                    val = safe_iat(df, great_grandchild_idx, great_grandchild_col)
                    gx, gy = parse_successful_total(val)
                    if gx is None or gy is None:
                        gx, gy = 0, 0
                    x += gx
                    y += gy

                total_processed += x
                total_received += y
            stream_name_out = ', '.join(str(s) for s in stream_names if s) if found_any else ''

        results.append({
            'Process Name': parent,
            'Stream Name': stream_name_out,
            'Date': date_part,
            'Start Time': start_time,
            'End Time': end_time,
            'Received Record': total_received,
            'Processed Record': total_processed
        })

    return results

def main():
    Tk().withdraw()
    file_paths = askopenfilenames(title="Select Excel file(s)", filetypes=[("Excel files", "*.xlsx")])
    if not file_paths:
        print("No files selected.")
        return

    all_results = []
    output_folder = None

    for file_path in file_paths:
        print(f"Processing file: {file_path}")
        results = process_file(file_path)
        all_results.extend(results)

        if output_folder is None:
            input_dir = os.path.dirname(file_path)
            output_folder = os.path.join(input_dir, "Formatted Data")
            os.makedirs(output_folder, exist_ok=True)

    if all_results:
        parent_order = list(parent_patterns.keys())

        txn_child_order = {
            'eagle_ml20_default_in_xml_warehouse_preproc_txn': 0,
            'eagle_ml20_default_in_xml_warehouse_preproc_txn_fee': 1
        }

        output_df = pd.DataFrame(all_results, columns=[
            'Process Name', 'Stream Name', 'Date', 'Start Time', 'End Time', 'Received Record', 'Processed Record'
        ])
        output_df['Process Name Lower'] = output_df['Process Name'].str.lower()
        output_df['Stream Name Lower'] = output_df['Stream Name'].str.lower()
        total_appearances = collections.Counter()
        for _, row in output_df.iterrows():
            key = (row['Process Name Lower'], row['Stream Name Lower'])
            total_appearances[key] += 1

        current_appearance = collections.defaultdict(int)

        def get_sort_key(row):
            parent_idx = len(parent_order)
            for idx, pname in enumerate(parent_order):
                if pname in row['Process Name Lower']:
                    parent_idx = idx
                    break

            child_idx = 0
            if 'inbnd_scd_txn' in row['Process Name Lower']:
                for k, v in txn_child_order.items():
                    if k in row['Stream Name Lower']:
                        child_idx = v
                        break
            key = (row['Process Name Lower'], row['Stream Name Lower'])
            current_appearance[key] += 1
            appearance_rank = total_appearances[key] - current_appearance[key] + 1
            return appearance_rank, parent_idx, child_idx

        output_df['sort_key'] = output_df.apply(get_sort_key, axis=1)
        output_df.sort_values(by='sort_key', inplace=True)
        output_df.drop(columns=['sort_key', 'Process Name Lower', 'Stream Name Lower'], inplace=True)

        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_folder, f"Trimmed_Record_{now_str}.xlsx")
        output_df.to_excel(output_file, index=False)
        print(f"Output saved to: {output_file}")
    else:
        print("No matching data found in the selected files.")

if __name__ == "__main__":
    main()
