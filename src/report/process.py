import csv
import re
import pandas as pd 
from src.report.model import Evaluation, Exercise, Player

DRILL_LIST = [
        '40_time',
        'bench_press',
        'broad_jump',
        'vertical_jump',
        'cone_drill',
        'shuttle_20',
        'shuttle_60'
    ]

    # POT
    # All-Pro
    # sky-high upside
    # great upside OR overlooked
    # great PFL player
    # most starting depth chart
    # long-term potential

    # CON
    # consistently impressive
    # generally solid
    # mistakes
    # film room
HARD_CODE_SCORECARD = {
    "All-Pro": 10,
    "sky-high upside": 8,
    "great upside": 6,
    "great PFL player": 4,
    "most starting depth chart": 2,
    "long-term potential": 1,
    "consistently impressive": 10,
    "generally solid": 8,
    "mistakes": 4,
    "film room": 1
}

def map_players(file_path):
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
                    evaluation = Evaluation(lines['evaluation'], lines['range'], lines['confidence'], lines['text'])
                    player.evaluation.append(evaluation)
                    lines['player_id'] = player
                ## Make a new player if they dont exist, using the player Id as the Key
                else:
                    evaluation = Evaluation(lines['evaluation'], lines['range'], lines['confidence'], lines['text'])
                    player = Player(lines['first_name'], lines['last_name'], lines['position'], lines['age'], lines['player_id'], lines['culture'], evaluation)
                    players[player.player_id] = player

                

    return players

def most_likely_raw_overall(player):
    weighted_scores = []
    for entry in player.evaluation:

        score = int(entry.score)
        r = int(entry.range)
        accuracy = int(entry.confidence)

        # Lower range means more certainty, so we divide accuracy by range_value to adjust.
        range_factor = 1 / (1 + r)

        # Adjust the weight by combining accuracy and range_factor
        weight = accuracy * range_factor

        # Add the weighted score to the list
        weighted_scores.append((score, weight))

    # Compute the weighted average of the scores
    total_weight = sum(weight for _, weight in weighted_scores)
    weighted_sum = sum(score * weight for score, weight in weighted_scores)

    most_likely_number = weighted_sum / total_weight

    # Even with most likely number 
    # I want it multipled by the wrong rate for a better score
    rounded_score = round(most_likely_number)
    text_report_score = 0
    fail_chance = []

    # Go through the reports again
    for evaluation in player.evaluation:
        eval_score = int(evaluation.score)
        # This allows for a safe range
        eval_range = int(evaluation.range)+1
        lower_limit = eval_score - eval_range
        high_limit = eval_score + eval_range

        # If its in the range of the reports, I want it, 
        # I also only care about text reports in this range
        if lower_limit <= rounded_score <= high_limit:
            text_report_score += calculate_report_score(evaluation.report,HARD_CODE_SCORECARD)
            fail_chance.append(1-(int(evaluation.confidence)*.01))


    potential_weighted = most_likely_number
    # Convert failure chance to a decimal
    failure_chance = 1.0
    for value in fail_chance:
        failure_chance *= value
    potential_weighted *= (1 - failure_chance)

    # Map to player
    player.potential_raw = most_likely_number
    player.potential_weighted = round(potential_weighted, 2)
    if len(fail_chance) > 0:
        player.report_score = text_report_score / len(fail_chance)
    
    # return statement for test
    # TODO REMOVE
    return most_likely_number, round(potential_weighted,2)

def calculate_report_score(paragraph, report_scorecard):

    total_score = 0
    paragraph = paragraph.lower()
    
    for phrase, score in report_scorecard.items():
        pattern = r'(?<!\w)' + re.escape(phrase.lower()).replace(r'\ ', r'\s+') + r'(?!\w)'
        matches = re.findall(pattern, paragraph)
        total_score += len(matches) * score
    
    return total_score

def map_combine(players, file_path):
    df_combine = pd.read_csv(file_path)
    with open(file_path, mode='r') as file:
        csvFile = csv.DictReader(file)

        for lines in csvFile:
            # TODO add exception
            if lines['player_id'] in players:
                player_row = lines
                player_id = player_row['player_id']
                # Map the combine
                combine = [
                    Exercise("40_time", player_row["40_time"]),
                    Exercise("bench_press", player_row['bench_press']),
                    Exercise("broad_jump", convert_string_to_float(player_row['broad_jump'])),
                    Exercise("vertical_jump", player_row['vertical_jump']),
                    Exercise("cone_drill", player_row['cone_drill']),
                    Exercise("shuttle_20", player_row['shuttle_20']),
                    Exercise("shuttle_60", player_row['shuttle_60'])
                ]

                players[player_id].combine.append(combine)
    return derive_max_min_ras(df_combine)

def derive_max_min_ras(combine_df):

    exercise_map = {}

    # Idea
    # combine_csv = sorted(combine_csv, key=lambda row: row['40_time'])
    # max_40 = combine_csv['40_time'][0]
    # min_40 = combine_csv['40_time'][-1]

    # lets clean it up

    for drill in DRILL_LIST:
        sorted_df = combine_df.sort_values(by=drill)
        if drill == 'broad_jump':
            # Need to convert because its a string
            min_drill_value = convert_string_to_float(sorted_df[drill].iloc[0])
            max_drill_value = convert_string_to_float(sorted_df[drill].iloc[-1])
        else:
            min_drill_value = sorted_df[drill].iloc[0].item()
            max_drill_value = sorted_df[drill].iloc[-1].item()
        exercise_map[drill] = (min_drill_value, max_drill_value)


    # For each exercise, sort, grab the first and last
    return exercise_map

def convert_string_to_float(string):
    
    # 10'5" -> 125
    parts = string.split("'")
    feet = int(parts[0]) * 12
    inches = int(parts[1].replace('"', '')) if parts[1] else 0
    # take substring after that and add to above
    
    return feet + inches

def convert_float_to_feet(number):
    # 125 -> 10.5
    inch = number % 12
    # modulus by 12, take remainder thats your (")
    feet = int((number - inch) / 12)
    # subtract remainder and divide by 12, that your (')
    # concat 
    return f"{feet}'{inch}\""

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
    count = 0
    for drill in DRILL_LIST:
        ras_exercise.append(derive_score_from_exercise(count, *exercise_map[drill], player))
        count += 1
    

    # sum of all scores / amount of exercise
    ras_dirty = sum(ras_exercise)/len(ras_exercise)
    player.ras_score = round(ras_dirty, 2)

def derive_score_from_exercise(exercise, min_value, max_value, player):
    
    # Some have better score when they are lower
    reverse = determine_reversal(exercise)
    float_value = float(player.combine[0][exercise].value)

    if reverse: 
        score = (max_value - float_value) / (max_value - min_value) * 10
    else:
        score = (float_value - min_value) / (max_value - min_value) * 10
    return max(0, min(10, score))  


def determine_reversal(exercise):
    if exercise == '40_time' or 'cone_drill' or 'shuttle_20' or 'shuttle_60':
        return True
    else:
        return False