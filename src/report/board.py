def create_board(players):
    # Sort by total score
    sorted_players = sorted(players, key=lambda player: player.total_score)

    # Save to CSV
    