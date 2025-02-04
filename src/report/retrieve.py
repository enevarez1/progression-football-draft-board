import csv

from src.report.model import Evaluation, Player

def map_players(file_path):

    ## Map of all players
    players = {}
    with open(file_path, mode='r') as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:

            ## If player exist, I want to add on to their evaluation array
            ## I also want to check if they have a culture
            ## It could just be media report that was old report.
            if lines['player_id'] in players:
                player = players[lines['player_id']]
                if player.culture == '':
                    player.culture = lines['culture']
                evaluation = Evaluation(lines['evaluation'], lines['range'], lines['confidence'])
                player.evaluation.append(evaluation)
                lines['player_id'] = player

            ## Make a new player if they dont exist, using the player Id as the Key
            evaluation = Evaluation(lines['evaluation'], lines['range'], lines['confidence'])
            player = Player(lines['first_name'], lines['last_name'], lines['position'], lines['age'], lines['player_id'], lines['culture'], evaluation)
            players[player.player_id] = player

    return players

def map_combine():
    return