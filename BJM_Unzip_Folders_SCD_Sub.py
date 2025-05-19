#This code will extract all the zipped file of SCD, Efront and C1R and divide them in separate folders and will create Sub Folder for SCD files based on extraction time
import os
import zipfile
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import stat

def extract_nested_zips(directory):
    """Recursively extract all zip files in directory"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                extract_path = os.path.splitext(file_path)[0]
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                os.remove(file_path)  # Remove the zip after extraction
                extract_nested_zips(extract_path)  # Recursively process new dir

def remove_readonly(func, path, _):
    """Clear readonly attribute and retry removal"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def main():
    # Create temporary extraction directory
    temp_dir = os.path.join(os.getcwd(), 'TEMP_EXTRACT')
    os.makedirs(temp_dir, exist_ok=True)

    # Select zip files
    root = tk.Tk()
    root.withdraw()
    zip_files = filedialog.askopenfilenames(
        title="Select ZIP Files",
        filetypes=[("ZIP Files", "*.zip")]
    )
    
    if not zip_files:
        print("No files selected. Exiting.")
        return

    # Extract all selected zips
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

    # Extract nested zips
    extract_nested_zips(temp_dir)

    # Create main folder with timestamp
    main_folder = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(main_folder, exist_ok=True)

    # Create subfolders
    categories = {
        'SCD': [
            'SCD_EGA_SECURITYMASTER',
            'SCD_EGA_FX_Rates',
            'SCD_EGA_Security_Rating',
            'SCD_EGA_Capital_Info',
            'SCD_EGA_Transactions_PL',
            'SCD_EGA_Transactions_Costs',
            'SCD_EGA_Holdings',
            'SCD_EGA_GL_Balances',
            'SCD_EGA_NAV',
            'SCD_EGA_SAA_TAA'
        ],
        'Efront': [
            'EFI_EGA_VALPOS',
            'EFI_EGA_TRX',
            'EFI_EGA_SECMAS'
        ],
        'C1R': [
            'C1R_TO_IDW_EQ',
            'C1R_TO_IDW_FI_DOMESTIC_CORPORATE_BOND',
            'C1R_TO_IDW_FI_GLOBAL_CORPORATE_BOND',
            'C1R_TO_IDW_FI_SUPRA'
        ]
    }

    for folder in categories.keys():
        os.makedirs(os.path.join(main_folder, folder), exist_ok=True)

    # Move CSV files to appropriate folders
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('.csv'):
                src_path = os.path.join(root, file)
                for category, patterns in categories.items():
                    if any(pattern in file for pattern in patterns):
                        if category == 'SCD':
                            # Extract last six digits and first two digits for SCD files
                            filename_parts = file.split('_')
                            last_part = filename_parts[-1].split('.')[0]  # Remove extension if present
                            if len(last_part) >= 6:
                                extraction_time = last_part[-6:-4]
                                # Determine am/pm based on extraction time
                                if int(extraction_time) < 12:
                                    time_suffix = "am"
                                else:
                                    time_suffix = "pm"
                                dest_path = os.path.join(main_folder, category, f"{extraction_time}_{time_suffix}", file)
                                dest_dir = os.path.dirname(dest_path)
                                os.makedirs(dest_dir, exist_ok=True)
                                shutil.move(src_path, dest_path)
                            else:
                                print(f"Skipping file {file} as it does not contain enough digits.")
                        else:
                            dest_path = os.path.join(main_folder, category, file)
                            shutil.move(src_path, dest_path)
                        break

    # Clean up temporary directory
    try:
        shutil.rmtree(temp_dir, onerror=remove_readonly)
    except Exception as e:
        print(f"Error removing temp directory: {e}")

    # Prompt to save main folder
    save_path = filedialog.askdirectory(title="Select Save Location")
    if save_path:
        final_path = os.path.join(save_path, main_folder)
        if os.path.exists(final_path):
            base, ext = os.path.splitext(final_path)
            counter = 1
            while os.path.exists(final_path):
                final_path = f"{base}_{counter}{ext}"
                counter += 1
        shutil.move(main_folder, final_path)
        print(f"Files saved to: {final_path}")
    else:
        print(f"Files remain in: {os.path.abspath(main_folder)}")

if __name__ == "__main__":
    main()
