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

def map_spinboxes_to_attibute_map():
    return {
        "overall_weight": score_vars["Potential Overall"].get(),
        "ras_weight": score_vars["RAS Score"].get(),
        "report_weight": score_vars["Report Score"].get(),
        "wonderlic": score_vars['Wonderlic'].get(),
        "all_pro": report_vars["All Pro"].get(),
        "sky_high": report_vars["Sky High"].get(),
        "great_upside": report_vars["Great Upside"].get(),
        "great_pfl": report_vars["Great PFL Player"].get(),
        "starting": report_vars["Most Starting Depth Chart"].get(),
        "long_term": report_vars["Not have long-term Potential"].get(),
        "consistent": report_vars["Consistently Impressive"].get(),
        "performance": report_vars["Performance Matches Reputation"].get(),
        "mistakes": report_vars["Makes Mistakes"].get(),
        "film": report_vars["Film Room"].get(),
        "trail": report_vars["Trailing Technique"].get(),
        "leader": report_vars["Leadership Potential"].get(),
        "strategy": culture_vars["Strategic"].get(),
        "energetic": culture_vars["Energetic"].get(),
        "professional": culture_vars["Professional"].get(),
        "aggressive": culture_vars["Aggressive"].get(),
        "adaptive": culture_vars["Adaptable"].get(),
        "unknown": culture_vars["Unknown"].get()
    }

def map_spinboxes_to_user_values():
    custom_values = UserValues()
    attribute_map = map_spinboxes_to_attibute_map()

    for attr, var in attribute_map.items():
        setattr(custom_values, attr, var)

    return custom_values

def generate_export_json():
    json_map = map_spinboxes_to_attibute_map()

    file_path = "exported_weights.json"

    with open(file_path, 'w') as json_file:
        json.dump(json_map, json_file, indent=4)
    directory_path = os.path.abspath(file_path)

    export_message = f"Your Exported Json file was generated at {directory_path}"

    tk.messagebox.showinfo("Alert", export_message)

    
def generate_board():

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
    directory_path = os.path.abspath("board.csv")
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
create_file_upload_section("Import JSON file")

button_frame = ttk.LabelFrame(content_frame, text='Actions', padding=15)
button_frame.pack(fill='x',padx=10, pady=10)

for i in range(3):
    button_frame.columnconfigure(i, weight=1)


ttk.Button(button_frame, text="Export Weights", command=generate_export_json).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Import Weights", command=generate_board).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Generate Board", command=generate_board).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

window.mainloop()