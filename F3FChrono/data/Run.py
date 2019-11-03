

class Run:

    def __init__(self):
        self._id = None
        self.run_time = None
        self.penalty = 0.0
        self.round_group = None
        self.competitor = None
        self.valid = False
        self.min_wind_speed = None
        self.max_wind_speed = None
        self.wind_direction = None
        self.start_time = None
        self.end_time = None
        self.reason = ""

    @property
    def id(self):
        return self._id

    def to_string(self):
        result = self.competitor.to_string() + '\t:\t' + str(self.run_time)
        if self.penalty > 0.0:
            result += '\tpenalty\t' + str(self.penalty)
        return result

