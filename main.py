#!/usr/bin/env python3

import tkinter.filedialog
from src.report.model import Exercise, UserValues
from src.report import process, report, retrieve

import tkinter as tkinter


def select_file(entry):
    filename = tkinter.filedialog.askopenfilename()
    entry.delete(0, tkinter.END)
    entry.insert(0, filename)

def generate_board():
    # grab values and map to UserValues
    custom_values = UserValues()
    custom_values.overall_weight = pot_ovr_spinbox.get()
    custom_values.ras_weight = ras_spinbox.get()
    custom_values.report_weight = report_spinbox.get()
    custom_values.all_pro = ap_spinbox.get()
    custom_values.sky_high = sh_spinbox.get()
    custom_values.great_upside = gu_spinbox.get()
    custom_values.great_pfl = gp_spinbox.get()
    custom_values.starting = ms_spinbox.get()
    custom_values.long_term = lt_spinbox.get()
    custom_values.consistent = cons_spinbox.get()
    custom_values.solid = gs_spinbox.get()
    custom_values.mistakes = mis_spinbox.get()
    custom_values.film = fr_spinbox.get()
    custom_values.strategy = st_spinbox.get()
    custom_values.energetic = en_spinbox.get()
    custom_values.professional = pr_spinbox.get()
    custom_values.aggressive = ag_spinbox.get()
    custom_values.adaptive = ad_spinbox.get()

    print(custom_values)

    print(scout_entry.get())
    print(combine_entry.get())

    
    players = process.map_players(scout_entry.get(), custom_values)
    combine_min_max_map= process.map_combine(players, combine_entry.get())

    for player in players.values():
        process.derive_ras(player, combine_min_max_map)
        process.most_likely_raw_overall(player, custom_values)

        # Reconvert the broad_jump because im not mean
        # Probably move this
        player.combine[0][2] = Exercise("broad_jump", process.convert_float_to_feet(player.combine[0][2].value))
        
        # Do the final total score for csv sorting, with user weights
        potential_weighted = player.potential_weighted * custom_values.overall_weight
        ras_score = player.ras_score * custom_values.ras_weight
        report_score = player.report_score * custom_values.report_weight
        player.total_score = potential_weighted + ras_score + report_score + player.culture_score

    sorted_players = sorted(players.values(), key=lambda player: player.total_score, reverse=True)
    report.generate_board(sorted_players)

window = tkinter.Tk()
window.title("Automatic Draft Board")

frame = tkinter.Frame(window)
frame.pack()



# Saving Score Weights
user_info_frame =tkinter.LabelFrame(frame, text="Overall Score Weights")
user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

help_label = tkinter.Label(user_info_frame, text="Select a value from 1 to 5")
help_label.grid(row=1, column=0)

pot_ovr_label = tkinter.Label(user_info_frame, text="Potential Overall Weight")
pot_ovr_spinbox = tkinter.Spinbox(user_info_frame, from_=1, to=5)
pot_ovr_label.grid(row=2, column=0)
pot_ovr_spinbox.grid(row=3, column=0)

ras_label = tkinter.Label(user_info_frame, text="RAS Score Weight")
ras_spinbox = tkinter.Spinbox(user_info_frame, from_=1, to=5)
ras_label.grid(row=2, column=1)
ras_spinbox.grid(row=3, column=1)

report_label = tkinter.Label(user_info_frame, text="Report Score Weight")
report_spinbox = tkinter.Spinbox(user_info_frame, from_=1, to=5)
report_label.grid(row=2, column=2)
report_spinbox.grid(row=3, column=2)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Saving Score Weights
report_info_frame =tkinter.LabelFrame(frame, text="Report Text Weights")
report_info_frame.grid(row= 4, column=0, padx=10, pady=10)

report_help_label = tkinter.Label(report_info_frame, text="Assign a value based on certain words in reports")
report_help_label.grid(row=5, column=0)

ap_label = tkinter.Label(report_info_frame, text="All-Pro")
ap_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
ap_label.grid(row=6, column=0)
ap_spinbox.grid(row=6, column=1)


sh_label = tkinter.Label(report_info_frame, text="Sky-High Upside")
sh_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
sh_label.grid(row=7, column=0)
sh_spinbox.grid(row=7, column=1)

gu_label = tkinter.Label(report_info_frame, text="Great PFL Player")
gu_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
gu_label.grid(row=8, column=0)
gu_spinbox.grid(row=8, column=1)

gp_label = tkinter.Label(report_info_frame, text="Great Upside")
gp_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
gp_label.grid(row=9, column=0)
gp_spinbox.grid(row=9, column=1)

ms_label = tkinter.Label(report_info_frame, text="Most Starting Depth Chart")
ms_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
ms_label.grid(row=10, column=0)
ms_spinbox.grid(row=10, column=1)

lt_label = tkinter.Label(report_info_frame, text="Not have long-term Potential")
lt_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
lt_label.grid(row=11, column=0)
lt_spinbox.grid(row=11, column=1)

cons_label = tkinter.Label(report_info_frame, text="Consistently Impressive")
cons_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
cons_label.grid(row=12, column=0)
cons_spinbox.grid(row=12, column=1)

gs_label = tkinter.Label(report_info_frame, text="Generally Solid")
gs_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
gs_label.grid(row=13, column=0)
gs_spinbox.grid(row=13, column=1)

mis_label = tkinter.Label(report_info_frame, text="Makes Mistakes")
mis_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
mis_label.grid(row=14, column=0)
mis_spinbox.grid(row=14, column=1)

fr_label = tkinter.Label(report_info_frame, text="Film Room")
fr_spinbox = tkinter.Spinbox(report_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
fr_label.grid(row=15, column=0)
fr_spinbox.grid(row=15, column=1)

for widget in report_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Culture
culture_info_frame = tkinter.LabelFrame(frame, text="Culture Weights")
culture_info_frame.grid(row= 16, column=0, padx=20, pady=10)

culture_help_label = tkinter.Label(culture_info_frame, text="Assign a value based on culture")
culture_help_label.grid(row=17, column=0)

ad_label = tkinter.Label(culture_info_frame, text="Adaptable")
ad_spinbox = tkinter.Spinbox(culture_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
ad_label.grid(row=18, column=0)
ad_spinbox.grid(row=18, column=1)

ag_label = tkinter.Label(culture_info_frame, text="Aggressive")
ag_spinbox = tkinter.Spinbox(culture_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
ag_label.grid(row=19, column=0)
ag_spinbox.grid(row=19, column=1)

en_label = tkinter.Label(culture_info_frame, text="Energetic")
en_spinbox = tkinter.Spinbox(culture_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
en_label.grid(row=20, column=0)
en_spinbox.grid(row=20, column=1)

pr_label = tkinter.Label(culture_info_frame, text="Professional")
pr_spinbox = tkinter.Spinbox(culture_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
pr_label.grid(row=21, column=0)
pr_spinbox.grid(row=21, column=1)

st_label = tkinter.Label(culture_info_frame, text="Strategic")
st_spinbox = tkinter.Spinbox(culture_info_frame, from_=-100, to=100, textvariable=tkinter.IntVar(value=0))
st_label.grid(row=22, column=0)
st_spinbox.grid(row=22, column=1)

for widget in culture_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

button = tkinter.Button(frame, text="Generate Board", command=generate_board)
button.grid(row= 16, column= 4, padx=20, pady=10)

scouting_file_frame = tkinter.LabelFrame(frame, text="Scouting Report")
scouting_file_frame.grid(row=0, column=4, pady=10)
scout_help_label = tkinter.Label(scouting_file_frame, text="Upload your scouting report", anchor="w")
scout_help_label.pack(side="left")

scout_entry = tkinter.Entry(scouting_file_frame, width=25)
button_file1 = tkinter.Button(scouting_file_frame, text="Browse", command=lambda: select_file(scout_entry))
for widget in scouting_file_frame.winfo_children():
    widget.grid_configure(pady=5)

combine_file_frame = tkinter.LabelFrame(frame, text="Combine Report")
combine_file_frame.grid(row=4, column=4, pady=10)
combine_help_label = tkinter.Label(combine_file_frame, text="Upload your combine report", anchor="w")
combine_help_label.pack(side="left")

combine_entry = tkinter.Entry(combine_file_frame, width=25)
button_file2 = tkinter.Button(combine_file_frame, text="Browse", command=lambda: select_file(combine_entry))
for widget in combine_file_frame.winfo_children():
    widget.grid_configure(pady=5)

window.mainloop()