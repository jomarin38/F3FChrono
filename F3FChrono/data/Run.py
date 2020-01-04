

class Run:

    def __init__(self):
        self.id = None
        self.chrono = None
        self.penalty = 0.0
        self.round_group = None
        self.competitor = None
        self.valid = False
        self.reason = ""

    def to_string(self):
        return self.competitor.to_string() + '\t:\t' + self.value_as_string()

    def value_as_string(self):
        res = self.chrono.to_string()
        if self.penalty > 0.0:
            res += '\tpenalty\t' + str(self.penalty)
        return res
