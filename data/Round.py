from .RoundGroup import RoundGroup
import os

class Round:

    round_counters = {}

    def __init__(self):
        self._event = None
        self._round_number = None
        self._groups = []

    @staticmethod
    def new_round(event):
        f3f_round = Round()
        f3f_round._event = event
        if event in Round.round_counters:
            previous_round = Round.round_counters[event]
        else:
            previous_round = 0
        Round.round_counters[event]=previous_round+1
        f3f_round._round_number = Round.round_counters[event]
        f3f_round._groups.append(RoundGroup(f3f_round))
        return f3f_round

    def add_run(self, run):
        #TODO : search in which group the run has to be added
        self._groups[0].add_run(run)

    def to_string(self):
        result = os.linesep + 'Round number ' + str(self._round_number) + os.linesep
        for g in self._groups:
            result += g.to_string() + os.linesep
        return result
