#this cide will promp to select file
#will display all the column, select the column
#will display available value, select the value
#will prompt to insert new value, insert new value
#will prompt to select folder to save file
#new folder will be created with the column name
#output file name will be same as input file name

import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd

class ColumnSelectorDialog(simpledialog.Dialog):
    def __init__(self, parent, title, columns):
        self.columns = columns
        self.selected_column = None
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Select the column to replace:").grid(row=0, column=0, padx=5, pady=5)
        self.combo = ttk.Combobox(master, values=self.columns, state="readonly")
        self.combo.grid(row=1, column=0, padx=5, pady=5)
        self.combo.current(0)  # Select first column by default
        return self.combo

    def apply(self):
        self.selected_column = self.combo.get()

def select_column(parent, columns):
    dialog = ColumnSelectorDialog(parent, "Select Column", columns)
    return dialog.selected_column

def main():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.update()

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        parent=root
    )

    if not file_path:
        print("No file selected. Exiting.")
        root.destroy()
        return

    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.csv']:
        df = pd.read_csv(file_path)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        messagebox.showerror("Error", "Unsupported file type.", parent=root)
        root.destroy()
        return

    # Use dropdown dialog to select column
    col_names = list(df.columns)
    col_name = select_column(root, col_names)
    if col_name is None:
        messagebox.showinfo("Cancelled", "No column selected. Exiting.", parent=root)
        root.destroy()
        return

    # Get value to replace using simpledialog (still string input)
    unique_vals = df[col_name].unique()
    value_to_replace = simpledialog.askstring(
        "Input",
        f"Enter the value to replace in column '{col_name}' (Available: {unique_vals}):",
        parent=root
    )
    if value_to_replace is None:
        messagebox.showinfo("Cancelled", "No value entered. Exiting.", parent=root)
        root.destroy()
        return

    if value_to_replace not in df[col_name].astype(str).values:
        messagebox.showerror("Error", f"Value '{value_to_replace}' not found in column '{col_name}'.", parent=root)
        root.destroy()
        return

    # Get new value
    new_value = simpledialog.askstring(
        "Input",
        f"Enter the new value to replace '{value_to_replace}' with:",
        parent=root
    )
    if new_value is None:
        messagebox.showinfo("Cancelled", "No new value entered. Exiting.", parent=root)
        root.destroy()
        return

    # Replace value
    df[col_name] = df[col_name].astype(str).replace(value_to_replace, new_value)

    # Select save location
    save_folder = filedialog.askdirectory(title="Select folder to save output", parent=root)
    if not save_folder:
        print("No save folder selected. Exiting.")
        root.destroy()
        return

    output_folder = os.path.join(save_folder, f"Replaced {col_name}")
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, os.path.basename(file_path))
    if ext == '.csv':
        df.to_csv(output_path, index=False)
    else:
        df.to_excel(output_path, index=False)

    messagebox.showinfo("Success", f"File saved to {output_path}", parent=root)
    root.destroy()

if __name__ == "__main__":
    main()
