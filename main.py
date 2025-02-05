from src.report import process

players = process.map_players('test_data.csv')
process.map_combine(players, 'combine_test.csv')


