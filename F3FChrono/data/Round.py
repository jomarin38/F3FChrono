import os
from F3FChrono.data.Run import Run
from F3FChrono.data.RoundGroup import RoundGroup
from F3FChrono.data.Chrono import Chrono
import copy


class Round:

    round_counters = {}

    def __init__(self):
        self.event = None
        self.round_number = None
        self.groups = []
        self._current_competitor_index = 0
        self._flight_order = []
        self.valid = False

    @staticmethod
    def new_round(event, add_initial_group=True):
        f3f_round = Round()
        f3f_round.event = event
        if event in Round.round_counters:
            previous_round = Round.round_counters[event]
        else:
            previous_round = 0
        Round.round_counters[event] = previous_round+1
        f3f_round.round_number = Round.round_counters[event]
        if add_initial_group:
            f3f_round.groups.append(RoundGroup(f3f_round, 1))
        f3f_round._flight_order += [c for c in event.get_competitors()]
        return f3f_round

    def add_group(self, round_group):
        self.groups.append(round_group)

    def handle_terminated_flight(self, competitor, chrono, penalty, valid):
        run = Run()
        run.competitor = competitor
        run.penalty = penalty
        run.chrono = copy.deepcopy(chrono)
        run.valid = valid
        self._add_run(run)

    def handle_refly(self, penalty):
        run = Run()
        run.competitor = self.get_current_competitor()
        run.penalty = penalty
        run.valid = False
        self._add_run(run)
        self._flight_order.insert(self._current_competitor_index + self.event.get_flights_before_refly() + 1,
                                  self.get_current_competitor().get_bib_number())

    def _add_run(self, run):
        #TODO : search in which group the run has to be added
        run.round_group = self.groups[0]
        self.groups[0].add_run(run)


    def to_string(self):
        result = os.linesep + 'Round number ' + str(self.round_number) + os.linesep
        for g in self.groups:
            result += g.to_string() + os.linesep
        return result

    def get_current_competitor(self):
        return self.event.get_competitor(self._flight_order[self._current_competitor_index])

    def set_current_competitor(self, competitor):
        self._current_competitor_index = self._flight_order.index(competitor.bib_number)

    def next_pilot(self):
        if self._current_competitor_index < len(self._flight_order) - 1:
            self._current_competitor_index += 1
        else:
            self.valid=True
            self.event.create_new_round()
            self._current_competitor_index = 0
        return self.get_current_competitor()

    def cancel_round(self):
        self.valid=False
        self.event.create_new_round()
        self._current_competitor_index = 0
        return self.get_current_competitor()
