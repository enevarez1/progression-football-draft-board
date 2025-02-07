from src.report import process

players = process.map_players('test_data.csv')
combine_min_max_map= process.map_combine(players, 'combine_test.csv')

for player in players.values():
    process.derive_ras(player, combine_min_max_map)

print(players)
