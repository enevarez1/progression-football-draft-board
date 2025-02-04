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

def derive_ras(combine):
    score = 0.0


    # Grab combine data from each exercise, store them each value in an array.
    # After set the min and the max, and map it to the exercise in a dictionary.
    # We need a reverse because sometimes lower number is better, e.g. 40 time

    ## Fill in formula 

    return score

def derive_score_from_exercise(exercise, exercise_map, player):
    
    # Some have better score when they are lower
    reverse = determine_reversal(exercise)

    if reverse: 
        score = (float)(exercise_map[exercise].max - player.exercise[exercise]) / (exercise_map[exercise].max - exercise_map[exercise].min) * 10
    else:
        score = (float)(player.exercise[exercise] - exercise_map[exercise].min) / (exercise_map[exercise].max - exercise_map[exercise].min) * 10
    return max(0, min(10, score))  

def determine_reversal(exercise):
    if exercise is '40_time' or 'cone_drill' or 'shuttle_20' or 'shuttle_60':
        return True
    else:
        return False