import os
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

security_ids = [
    "IC_AHP-ASNB", "IC_AHP-OMBAK", "IC_AHP-PHNB", "IC_ASB-ASNB", "IC_ASB-PNB", "IC_ASB2-ASNB",
    "IC_ASB2-PNB", "IC_ASB3-PNB", "IC_ASB3D-ASNB", "IC_ASM-ASNB", "IC_ASM-PNB", "IC_ASM2-ASNB",
    "IC_ASM2-PNB", "IC_ASM3-ASNB", "IC_ASM3-PNB", "IC_ASN-ASNB", "IC_ASN-PNB", "IC_ASNE2-ASNB",
    "IC_ASNE2-PNB", "IC_ASNE3-ASNB", "IC_ASNE3-PNB", "IC_ASNE5-ASNB", "IC_ASNE5-PNB", "IC_ASNEG-PNB",
    "IC_ASNEG1-ASNB", "IC_ASNEG1-PNB", "IC_ASNEM-PNB", "IC_ASNEM1-ASNB", "IC_ASNI1-ASNB", "IC_ASNI1-PNB",
    "IC_ASNI2-ASNB", "IC_ASNI2-PNB", "IC_ASNI3-PNB", "IC_ASNI3G1-ASNB", "IC_ASNI3G1-PNB", "IC_ASNS1-ASNB",
    "IC_ASNS1-PNB", "IC_ASNS2-ASNB", "IC_ASNS2-PNB", "IC_ASNSK1-PNB", "IC_PHNB-AHP", "IC_PNB-AHP",
    "IC_PNB-YTI"
]

def add_slash(security_id):
    if isinstance(security_id, str) and security_id.startswith("IC_"):
        return "I/C" + security_id[2:]
    return security_id

root = Tk()
root.withdraw()

file_paths = askopenfilenames(
    title='Select file(s) to process',
    filetypes=[('CSV files', '*.csv'), ('Excel files', '*.xlsx;*.xls')]
)

if not file_paths:
    print("No files selected. Exiting.")
    exit()

for file_path in file_paths:
    if file_path.lower().endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    if 'Security ID' in df.columns:
        df['Security ID'] = df['Security ID'].apply(lambda x: add_slash(x) if x in security_ids else x)

    # Create output folder inside the input file's folder
    input_folder = os.path.dirname(file_path)
    output_folder = os.path.join(input_folder, "Add Slash")
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, os.path.basename(file_path))
    if file_path.lower().endswith('.csv'):
        df.to_csv(output_path, index=False)
    else:
        df.to_excel(output_path, index=False)

print(f"Processed {len(file_paths)} file(s) and saved to their respective 'Add Slash' folders.")
