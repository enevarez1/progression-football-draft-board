#!/usr/bin/env python3

from tkinter import ttk
from src.report.model import Exercise, UserValues
from src.report import process, report

import tkinter as tk
import tkinter.filedialog
import os
import json


def select_file(entry):
    filename = tk.filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def map_spinboxes_to_attributes(as_int=False):
    attribute_map = {
        "overall_weight": score_vars["Potential Overall"],
        "ras_weight": score_vars["RAS Score"],
        "report_weight": score_vars["Report Score"],
        "wonderlic": score_vars["Wonderlic"],
        "all_pro": report_vars["All Pro"],
        "sky_high": report_vars["Sky High"],
        "great_upside": report_vars["Great Upside"],
        "great_pfl": report_vars["Great PFL Player"],
        "starting": report_vars["Most Starting Depth Chart"],
        "long_term": report_vars["Not have long-term Potential"],
        "consistent": report_vars["Consistently Impressive"],
        "performance": report_vars["Performance Matches Reputation"],
        "mistakes": report_vars["Makes Mistakes"],
        "film": report_vars["Film Room"],
        "trail": report_vars["Trailing Technique"],
        "leader": report_vars["Leadership Potential"],
        "strategy": culture_vars["Strategic"],
        "energetic": culture_vars["Energetic"],
        "professional": culture_vars["Professional"],
        "aggressive": culture_vars["Aggressive"],
        "adaptive": culture_vars["Adaptable"],
        "unknown": culture_vars["Unknown"]
    }
    
    return {key: var.get() if as_int else var for key, var in attribute_map.items()}


def map_spinboxes_to_user_values():
    custom_values = UserValues()
    attribute_map = map_spinboxes_to_attributes(as_int=True)

    for attr, var in attribute_map.items():
        setattr(custom_values, attr, var)

    return custom_values

def generate_export_json():
    json_map = map_spinboxes_to_attributes(as_int=True)

    file_name = tk.simpledialog.askstring("Save As", "Enter a name for the exported weights file (without extension):")

    if not file_name:
        return  

    file_path = f"{file_name}.json"

    try:
        with open(file_path, 'w') as json_file:
            json.dump(json_map, json_file, indent=4)
        directory_path = os.path.abspath(file_path)
        export_message = f"Your Exported JSON file was saved at:\n{directory_path}"
        tk.messagebox.showinfo("Export Successful", export_message)
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to save file: {e}")

def import_custom_values():
    file_path = tk.filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=[("JSON files", "*.json"), ("All Files", "*.*")]
    )

    if not file_path:
        return
    
    custom_values = {}

    try:
        with open(file_path, 'r') as file:
            custom_values = json.load(file)
    except FileNotFoundError:
        tk.messagebox.showerror("Error", f"Error: File not found. Please select a valid file.")
        return None
    except json.JSONDecodeError:
        tk.messagebox.showinfo("Error", f"Error: Invalid JSON format in {file_path}")
        return None
    
    gearbox_values = map_spinboxes_to_attributes(as_int=False)
    for key, value in custom_values.items():
        if key in gearbox_values:
            gearbox_values[key].set(value)

    tk.messagebox.showinfo("Success", "Weights imported successfully and updated!")

def generate_board():
    file_name = tk.simpledialog.askstring("Save As", "Enter a name for your board csv (without extension):")

    if not file_name:
        return  

    file_path = f"{file_name}.csv"

    custom_values = map_spinboxes_to_user_values()
    
    players = process.map_players(file_upload_entries["Scouting Report"].get(), custom_values)
    combine_min_max_map= process.map_combine(players, file_upload_entries["Draft Class Report"].get())

    for player in players.values():
        process.derive_ras(player, combine_min_max_map)
        process.most_likely_raw_overall(player, custom_values)

        # Reconvert the broad_jump because im not mean
        # Probably move this
        player.combine[0][2] = Exercise("broad_jump", process.convert_float_to_feet(player.combine[0][2].value))
        
        # Do the final total score for csv sorting, with user weights
        potential_weighted = player.potential_weighted * custom_values.overall_weight
        ras_score = player.ras_score * custom_values.ras_weight
        report_score = round(player.report_score * custom_values.report_weight, 2)
        wonderlic_score = player.wonderlic * custom_values.wonderlic
        player.total_score = potential_weighted + ras_score + report_score + player.culture_score + wonderlic_score

    sorted_players = sorted(players.values(), key=lambda player: player.total_score, reverse=True)
    report.generate_board(sorted_players)
    directory_path = os.path.abspath(file_path)
    board_message = f"Your board file was generated at {directory_path}"

    tk.messagebox.showinfo("Alert", board_message)

window = tk.Tk()
window.title("Automatic Draft Board")
window.geometry("1000x750")
window.minsize(800, 600)

main_frame = ttk.Frame(window)
main_frame.pack(fill="both", expand=1)

canvas = tk.Canvas(main_frame, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

content_frame = ttk.Frame(canvas, padding=20)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

style = ttk.Style()
style.configure("TLabel", font=("Arial", 11))
style.configure("TButton", font=("Arial", 11), padding=5)
style.configure("TEntry", font=("Arial", 11))
style.configure("TLabelframe", font=("Arial", 12, "bold"))
style.configure("TLabelframe.Label", font=("Arial", 12, "bold"))

def create_spinbox_row(frame, label_text, var, row, col):
    ttk.Label(frame, text=label_text).grid(row=row, column=col*2, sticky="w", padx=10, pady=7)
    ttk.Spinbox(frame, from_=-100, to=100, width=6, textvariable=var, justify="center").grid(row=row, column=col*2+1, padx=5, pady=7)

def create_var_dict(keys, default=0):
    return {key: tk.IntVar(value=default) for key in keys}

score_vars = create_var_dict(["Potential Overall", "RAS Score", "Report Score", "Wonderlic"], default=1)
report_vars = create_var_dict(["All Pro", "Sky High","Leadership Potential", "Great PFL Player", "Great Upside",
                               "Most Starting Depth Chart", "Not have long-term Potential",
                               "Consistently Impressive", 
                               "Performance Matches Reputation", "Makes Mistakes", "Film Room", "Trailing Technique"])
culture_vars = create_var_dict(["Adaptable", "Aggressive", "Energetic", "Professional", "Strategic", "Unknown"])

def create_section(title, vars_dict, cols=2):
    frame = ttk.LabelFrame(content_frame, text=title, padding=15)
    frame.pack(fill="x", padx=10, pady=10)
    for i, (label, var) in enumerate(vars_dict.items()):
        row, col = divmod(i, cols)
        create_spinbox_row(frame, label, var, row, col)

create_section("Overall Score Weights", score_vars, cols=4)
create_section("Report Text Weights", report_vars, cols=3)
create_section("Culture Weights", culture_vars, cols=3)

file_upload_entries = {}
def create_file_upload_section(title):
    frame = ttk.LabelFrame(content_frame, text=title, padding=15)
    frame.pack(fill="x", padx=10, pady=10)
    entry = ttk.Entry(frame, width=40)
    entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
    ttk.Button(frame, text="Browse", command=lambda: select_file(entry)).pack(side="left", padx=5)
    file_upload_entries[title] = entry
create_file_upload_section("Scouting Report")
create_file_upload_section("Draft Class Report")

button_frame = ttk.LabelFrame(content_frame, text='Actions', padding=15)
button_frame.pack(fill='x',padx=10, pady=10)

for i in range(3):
    button_frame.columnconfigure(i, weight=1)


ttk.Button(button_frame, text="Export Weights", command=generate_export_json).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Import Weights", command=import_custom_values).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Generate Board", command=generate_board).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

window.mainloop()