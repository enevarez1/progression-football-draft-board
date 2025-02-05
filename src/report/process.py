from report.model import Evaluation, Exercise, Player

DRILL_LIST = [
        '40_time',
        'bench_press',
        'broad_jump',
        'vertical_drill',
        'cone_drill',
        'shuttle_20',
        'shuttle_60'
    ]

def map_players(csvFile):
    players = {}
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

def most_likely_raw_overall(evaluations):
    weighted_scores = []

    for entry in evaluations:
        score = entry['score']
        range = entry['range']
        accuracy = entry['confidence']

        # Lower range means more certainty, so we divide accuracy by range_value to adjust.
        range_factor = 1 / (1 + range)

        # Adjust the weight by combining accuracy and range_factor
        weight = accuracy * range_factor

        # Add the weighted score to the list
        weighted_scores.append((score, weight))

    # Compute the weighted average of the scores
    total_weight = sum(weight for _, weight in weighted_scores)
    weighted_sum = sum(score * weight for score, weight in weighted_scores)

    most_likely_number = weighted_sum / total_weight
    return most_likely_number

def map_combine(players, csvFile):
    for lines in csvFile:
        # TODO add exception
        if lines['player_id'] in players:
            player_row = lines['player_id']
            # Map the combine
            combine = [
                Exercise("40_time", player_row['40_time']),
                Exercise("bench_press", player_row['bench_press']),
                Exercise("broad_jump", player_row['broad_jump']),
                Exercise("vertical_jump", player_row['vertical_jump']),
                Exercise("cone_drill", player_row['cone_drill']),
                Exercise("shuttle_20", player_row['shuttle_20']),
                Exercise("shuttle_60", player_row['shuttle_60'])
            ]
            players['player_id'].combine = combine
    return players

def derive_score_from_report(report_text):
    # Hardcoded Values for now
    values = {
        "all-pro": 10,
        "sky-high": 9,
        "starter": 8,
        "low-ceiling": 7,
        "film-room": 3,
        "calm": 7,
        "consistenly-impressive": 8
    }

    score = 0

    ## Search through paragraph looking for those key words and add to score


    return score

def derive_max_min_ras(combine_csv):

    exercise_map = {}

    # Idea
    # combine_csv = sorted(combine_csv, key=lambda row: row['40_time'])
    # max_40 = combine_csv['40_time'][0]
    # min_40 = combine_csv['40_time'][-1]

    # lets clean it up

    for drill in DRILL_LIST:
        sorted_drill = sorted(combine_csv, key=lambda row: row[drill])
        min_drill_value = sorted_drill[0]
        max_drill_value = sorted_drill[-1]
        exercise_map[drill] = (min_drill_value, max_drill_value)


    # For each exercise, sort, grab the first and last
    return exercise_map

def derive_ras(player, exercise_map):
    score = 0.0

    # run all exercises with the min and max
    # ras_exercises = [
    #     derive_score_from_exercise('40_time', *exercise_map['40_time'], player),
    #     derive_score_from_exercise('bench_press', *exercise_map['bench_press'], player),
    #     derive_score_from_exercise('broad_jump', *exercise_map['broad_jump'], player),
    #     derive_score_from_exercise('vertical_jump', *exercise_map['vertical_jump'], player),
    #     derive_score_from_exercise('cone_drill', *exercise_map['cone_drill'], player),
    #     derive_score_from_exercise('shuttle_20', *exercise_map['shuttle_20'], player),
    #     derive_score_from_exercise('shuttle_60', *exercise_map['shuttle_60'], player)
    # ]

    ras_exercise = []
    for drill in DRILL_LIST:
        ras_exercise.append(derive_score_from_exercise(drill, *exercise_map[drill], player))
    

    # sum of all scores / amount of exercise
    return sum(ras_exercise)/len(ras_exercise)

def derive_score_from_exercise(exercise, min_value, max_value, player):
    
    # Some have better score when they are lower
    reverse = determine_reversal(exercise)

    if reverse: 
        score = (float)(max_value - player.exercise[exercise].value) / (max_value - min_value) * 10
    else:
        score = (float)(player.exercise[exercise].value - min_value) / (max_value - min_value) * 10
    return max(0, min(10, score))  

def determine_reversal(exercise):
    if exercise is '40_time' or 'cone_drill' or 'shuttle_20' or 'shuttle_60':
        return True
    else:
        return False