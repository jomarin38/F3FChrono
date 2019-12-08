

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
        result = self.competitor.to_string() + '\t:\t' + self.chrono.to_string()
        if self.penalty > 0.0:
            result += '\tpenalty\t' + str(self.penalty)
        return result

