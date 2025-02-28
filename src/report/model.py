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
        self.link = ""
        self.wonderlic = 0
        self.potential_raw = 0.0
        self.potential_weighted = 0.0
        self.ras_score = 0.0
        self.report_score = 0.0
        self.culture_score = 0.0
        self.total_score = 0.0

    # def __setattr__(self, name, value):
    #     if name == 'combine':
    #         super().__setattr__(name, value)

@auto_str
class Evaluation:
    def __init__(self, score, range, confidence, report):
        self.score = score
        self.range = range
        self.confidence = confidence
        self.report = report

@auto_str
class Exercise:
    def __init__(self, name, value):
        self.name = name
        self.value = value

@auto_str
class UserValues:
    def __init__(self):
        self.overall_weight = 1
        self.ras_weight = 1
        self.report_weight = 1
        self.wonderlic = 1
        self.all_pro = 1
        self.sky_high = 1
        self.great_upside = 1
        self.great_pfl = 1
        self.starting = 1
        self.long_term = 1
        self.consistent = 1
        self.performance = 1
        self.mistakes = 1
        self.film = 1
        self.trail = 1
        self.leader = 1
        self.strategy = 1
        self.energetic = 1
        self.professional = 1
        self.aggressive = 1
        self.adaptive = 1
        self.unknown = 1

        # All Pro in Report
        # Sky High In Report
        # Great Upside in Report
        # Great PFL in Report
        # Starting Depth in Report
        # No Long Term in Report
        # Consistently Impressive in Report
        # Generally Solid in Report
        # Makes Mistakes in Report
        # Film Room in Report
        # Strategy Culture
        # Energetic Culture
        # Professional Culture
        # Aggressive Culture
        # Adaptive Culture