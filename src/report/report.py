import csv

HEADER = [
        'Player ID',
        'First Name',
        'Last Name',
        'Age',
        'Position',
        'Culture',
        'Potential Raw Overall',
        'Potential Raw Weighted',
        'RAS Score',
        'Report Score',
        'Wonderlic Score',
        'Total Board Score',
        'Link'
    ]

# Method to write to CSV
def generate_board(players):
    csv_data = []
    for player in players:
        row = flatten_player(player)
        row['Player ID'] = player.player_id
        csv_data.append(row)

    with open('board.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(csv_data)

# Method to flatten object to rows
def flatten_player(player):
    return {
        'First Name': player.first_name,
        'Last Name': player.last_name,
        'Age': player.age,
        'Position': player.position,
        'Culture': player.culture,
        'Potential Raw Overall': player.potential_raw,
        'Potential Raw Weighted': player.potential_weighted,
        'RAS Score': player.ras_score,
        'Report Score': player.report_score,
        'Wonderlic Score': player.wonderlic,
        'Total Board Score': player.total_score,
        'Link': player.link
    }