#!/usr/bin/env python3

from src.report.model import Exercise
from src.report import process, report, retrieve

custom_values = retrieve.retrieve_custom_values()

players = process.map_players('test_data.csv', custom_values)
combine_min_max_map= process.map_combine(players, 'combine_test.csv')

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
