import os
from F3FChrono.data.Run import Run
from F3FChrono.data.RoundGroup import RoundGroup


class Round:

    round_counters = {}

    def __init__(self):
        self._event = None
        self._round_number = None
        self._groups = []
        self._current_competitor_index = 0
        self._flight_order = []

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
        f3f_round._flight_order += [c for c in event.get_competitors()]
        return f3f_round

    def handle_terminated_flight(self, competitor, chrono, penalty, valid):
        run = Run()
        run.competitor = competitor
        run.penalty = penalty
        run.chrono = chrono
        run.valid = valid
        self._add_run(run)

    def handle_refly(self, penalty):
        run = Run()
        run.competitor = self.get_current_competitor()
        run.penalty = penalty
        run.valid = False
        self._add_run(run)
        self._flight_order.insert(self._current_competitor_index + self._event.get_flights_before_refly() + 1,
                                  self.get_current_competitor().get_bib_number())

    def _add_run(self, run):
        #TODO : search in which group the run has to be added
        self._groups[0]._add_run(run)

    def to_string(self):
        result = os.linesep + 'Round number ' + str(self._round_number) + os.linesep
        for g in self._groups:
            result += g.to_string() + os.linesep
        return result

    def get_current_competitor(self):
        return self._event.get_competitor(self._flight_order[self._current_competitor_index])

    def next_pilot(self):
        #TODO : detect end of round
        if self._current_competitor_index < len(self._flight_order) - 1:
            self._current_competitor_index += 1
        return self.get_current_competitor()
