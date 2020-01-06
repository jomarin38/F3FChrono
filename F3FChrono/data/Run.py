

class Run:

    def __init__(self):
        self.id = None
        self.chrono = None
        self.penalty = 0.0
        self.round_group = None
        self.competitor = None
        self.valid = False
        self.reason = ""
        self.score = None

    def to_string(self):
        return self.competitor.display_name() + '\t:\t' + self.value_as_string()

    def value_as_string(self):
        res = self.chrono.run_time_as_string()
        if self.penalty > 0.0:
            res += '\tP\t' + str(self.penalty)
        return res

    def score_as_string(self):
        return '{:04.2f}'.format(self.score)

    def get_flight_time(self):
        return self.chrono.run_time
