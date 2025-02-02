def most_likely_raw_overall(objects):
    total_weight = 0
    weighted_sum = 0
    
    for obj in objects:
        score = obj['score']
        range_ = obj['range']
        confidence = obj['confidence']
        
        # The range is the interval [score - range, score + range]
        # We'll consider the mid-point of the range as the likely value.
        range_midpoint = score
        
        # Weighted score: range_midpoint * confidence
        weighted_sum += range_midpoint * confidence
        total_weight += confidence
    
    # The most likely score is the weighted average
    if total_weight == 0:
        return None  
    return weighted_sum / total_weight

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