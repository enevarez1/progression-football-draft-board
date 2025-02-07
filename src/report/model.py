def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls

@auto_str
class Player:
    def __init__(self, first_name, last_name, position, age, player_id, culture, evaluation):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.age = age
        self.player_id = player_id
        self.culture = culture
        self.evaluation = [evaluation]
        self.combine = []
        self.potential_raw = 0.0
        self.potential_weighted = 0.0
        self.ras_score = 0.0
        self.report_score = 0.0
        self.total_score = 0.0

    # def __setattr__(self, name, value):
    #     if name == 'combine':
    #         super().__setattr__(name, value)

@auto_str
class Evaluation:
    def __init__(self, score, range, confidence):
        self.score = score
        self.range = range
        self.confidence = confidence

@auto_str
class Exercise:
    def __init__(self, name, value):
        self.name = name
        self.value = value