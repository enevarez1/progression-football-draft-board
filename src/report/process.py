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


    ## Fill in formula

    return score
