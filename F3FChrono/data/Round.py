import os
from F3FChrono.data.Run import Run
from F3FChrono.data.RoundGroup import RoundGroup
from F3FChrono.data.Chrono import Chrono
from F3FChrono.data.dao.RoundDAO import RoundDAO

class Round:

    round_counters = {}
    valid_round_counters = {}
    round_dao = RoundDAO()

    def __init__(self):
        self.event = None
        self.round_number = None
        self.valid_round_number = None
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

        for bib in range(event.bib_start, event.get_nb_competitors()+1):
            f3f_round._flight_order += [bib]
        for bib in range(1, event.bib_start):
            f3f_round._flight_order += [bib]
        #print(f3f_round._flight_order)
        return f3f_round

    def add_group(self, round_group):
        self.groups.append(round_group)

    def handle_terminated_flight(self, competitor, chrono, penalty, valid, insert_database=False):
        run = Run()
        run.competitor = competitor
        run.penalty = penalty
        run.chrono = chrono
        run.valid = valid
        self._add_run(run, insert_database)


    def handle_refly(self, penalty):
        run = Run()
        run.competitor = self.get_current_competitor()
        run.penalty = penalty
        run.valid = False
        self._add_run(run)
        self._flight_order.insert(self._current_competitor_index + self.event.get_flights_before_refly() + 1,
                                  self.get_current_competitor().get_bib_number())

    def _add_run(self, run, insert_database=False):
        #TODO : search in which group the run has to be added
        run.round_group = self.groups[-1]
        self.groups[-1].add_run(run, insert_database)

    def to_string(self):
        result = os.linesep + 'Round number ' + str(self.round_number) + os.linesep
        for g in self.groups:
            result += g.to_string() + os.linesep
        return result

    def get_current_competitor(self):
        return self.event.get_competitor(self._flight_order[self._current_competitor_index])

    def set_current_competitor(self, competitor):
        self._current_competitor_index = self._flight_order.index(competitor.bib_number)

    def next_pilot(self, insert_database=False):
        if self._current_competitor_index < len(self._flight_order) - 1:
            self._current_competitor_index += 1
        else:
            self.validate_round(insert_database)
            self.event.create_new_round(insert_database)
            self._current_competitor_index = 0
        return self.get_current_competitor()

    def next_pilot_database(self):
        nb_run=len(self.groups[len(self.groups)-1].runs)
        #if self._current_competitor_index < len(self._flight_order) - 1:
        if  nb_run< len(self._flight_order):
            self._current_competitor_index = nb_run
        else:
            self.event.create_new_round(insert_database=True)
            self._current_competitor_index = 0
        return self.get_current_competitor()

    def cancel_round(self):
        self.valid=False
        self.valid_round_number=None
        Round.round_dao.update(self)
        self.event.create_new_round(insert_database=True)
        self._current_competitor_index = 0
        return self.get_current_competitor()

    def validate_round(self, insert_database=False):
        self.valid = True
        if self.event in Round.valid_round_counters:
            previous_round = Round.valid_round_counters[self.event]
        else:
            previous_round = 0
        self.valid_round_number = previous_round+1
        Round.valid_round_counters[self.event] = self.valid_round_number
        self.event.valid_rounds.append(self)
        if insert_database:
            Round.round_dao.update(self)

    def has_run(self):
        return(self.groups[-1].has_run())

    def get_best_runs(self):
        result = []
        for group in self.groups:
            result.append(group.get_best_run())
        return result
