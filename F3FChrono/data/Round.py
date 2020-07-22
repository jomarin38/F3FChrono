import os
from F3FChrono.data.Run import Run
from F3FChrono.data.RoundGroup import RoundGroup
from F3FChrono.data.Chrono import Chrono
from F3FChrono.data.dao.CompetitorDAO import CompetitorDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO
import requests


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

        return f3f_round

    def add_group(self, round_group):
        self.groups.append(round_group)

    def get_serialized_flight_order(self):
        res = ''
        for bib_number in self._flight_order:
            res += str(bib_number) + ','
        return res.rstrip(',')

    def get_flight_order(self):
        return self._flight_order

    def get_remaining_bibs_to_fly(self):
        if not self.valid:
            if self.has_run():
                currently_flying_bib = self._current_competitor_index+1
            else:
                currently_flying_bib = self._current_competitor_index
            return self._flight_order[currently_flying_bib:]
        else:
            return []

    def set_flight_order_from_db(self, serialized_flight_order):
        splitted_line = serialized_flight_order.split(',')
        self._flight_order.clear()
        for str_bib_number in splitted_line:
            self._flight_order.append(int(str_bib_number))

    def set_flight_order_from_scratch(self):
        self._flight_order.clear()
        for bib in [bib_number for bib_number in sorted(self.event.competitors)
                    if bib_number >= self.event.bib_start]:
            self._flight_order += [bib]
        for bib in [bib_number for bib_number in sorted(self.event.competitors)
                    if bib_number < self.event.bib_start]:
            self._flight_order += [bib]

    def handle_terminated_flight(self, competitor, chrono, penalty, valid, insert_database=False):
        run = Run()
        run.competitor = competitor
        run.penalty = penalty
        run.chrono = chrono
        run.valid = valid
        self._add_run(run, insert_database)

    def display_name(self):

        if self.valid:
            round_number = str(self.valid_round_number)
        else:
            round_number = 'not valid'

        return 'Round ' + str(round_number)

    def handle_refly(self, penalty, insert_database=False):
        run = Run()
        run.competitor = self.get_current_competitor()
        run.penalty = penalty
        run.valid = False
        self._add_run(run, insert_database=insert_database)
        self.give_refly(self.get_current_competitor())

    def give_refly(self, competitor):
        self._flight_order.insert(self._current_competitor_index + self.event.get_flights_before_refly() + 1,
                                  competitor.get_bib_number())
        RoundDAO().update(self)

    def _add_run(self, run, insert_database=False):
        # TODO : search in which group the run has to be added
        run.round_group = self.groups[-1]
        self.groups[-1].add_run(run, insert_database)
        self.set_current_competitor(run.competitor)

    def add_run_from_web(self, run):
        # TODO : search in which group the run has to be added
        run.round_group = self.groups[-1]
        self.groups[-1].add_run(run, True)

    def to_string(self):
        result = os.linesep + 'Round number ' + str(self.round_number) + os.linesep
        for g in self.groups:
            result += g.to_string() + os.linesep
        return result

    def get_current_competitor(self):
        return self.event.get_competitor(self._flight_order[self._current_competitor_index])

    def set_current_competitor(self, competitor):
        self._current_competitor_index = self._current_competitor_index + \
                                        self._flight_order[self._current_competitor_index:].index(competitor.bib_number)

    def set_flight_order_index(self, index):
        self._current_competitor_index = index

    def next_pilot(self, insert_database=False, visited_competitors=[]):
        if self._current_competitor_index < len(self._flight_order) - 1:
            self._current_competitor_index += 1
            current_competitor = self.get_current_competitor()
            current_round = self
        else:
            self.validate_round(insert_database)
            current_round = self.event.create_new_round(insert_database)
            current_competitor = current_round.get_current_competitor()
        if current_competitor.present:
            return current_competitor
        else:
            if current_competitor not in visited_competitors:
                # Give him a 0
                current_round.set_null_flight(current_competitor)
                visited_competitors.append(current_competitor)
                return current_round.next_pilot(insert_database, visited_competitors)
            else:
                #In this case, nobody is set to present ...
                return current_competitor

    def set_null_flight(self, competitor):
        self.handle_terminated_flight(
            competitor,
            Chrono(), 0, False, insert_database=True)

    def number_of_performed_runs(self):
        result = 0
        for bib_number, runs_list in self.groups[-1].runs.items():
            result += len(runs_list)
        return result

    def next_pilot_database(self):
        nb_run = self.number_of_performed_runs()
        # if self._current_competitor_index < len(self._flight_order) - 1:
        if nb_run < len(self._flight_order):
            self._current_competitor_index = nb_run
        else:
            self.event.create_new_round(insert_database=True)
            self._current_competitor_index = 0
        return self.get_current_competitor()

    def cancel_round(self):
        self.do_cancel_round()
        self.event.create_new_round(insert_database=True)
        self._current_competitor_index = 0
        return self.get_current_competitor()

    def do_cancel_round(self):
        self.valid = False
        self.valid_round_number = None
        Round.round_dao.update(self)

    def validate_round(self, insert_database=False):
        self.valid = True
        if self.event in Round.valid_round_counters:
            previous_round = Round.valid_round_counters[self.event]
        else:
            previous_round = 0
        self.valid_round_number = previous_round + 1
        Round.valid_round_counters[self.event] = self.valid_round_number
        self.event.valid_rounds.append(self)
        if insert_database:
            Round.round_dao.update(self)

    def has_run(self):
        res = False
        for f3f_group in self.groups:
            res = res or f3f_group.has_run()
        return res

    def has_run_competitor(self, competitor):
        res = False
        for f3f_group in self.groups:
            res = res or f3f_group.has_run_competitor(competitor)
        return res

    def get_valid_run(self, competitor):
        valid_run = None
        for f3f_group in self.groups:
            valid_run = f3f_group.get_valid_run(competitor)
        return valid_run

    def get_best_runs(self):
        result = []
        for group in self.groups:
            result.append(group.get_best_run())
        return result

    def get_penalty(self, competitor):
        penalty = 0
        for group in self.groups:
            penalty += group.get_penalty(competitor)
        return penalty

    def give_penalty(self, competitor, penalty):
        f3f_run = self.get_valid_run(competitor)
        if f3f_run is None:
            runs = []
            for group in self.groups:
                runs_in_group = group.runs[competitor]
                if runs_in_group is not None:
                    runs += runs_in_group
            if len(runs) > 0:
                f3f_run = runs[0]
            else:
                raise Exception('Can t give penalty to a pilot that did not flew')

        if penalty == 0:
            f3f_run.penalty = 0
        else:
            f3f_run.penalty += penalty

    def export_to_f3x_vault(self, login, password):
        for group in self.groups:
            for bib_number, competitor in self.event.competitors.items():
                fetched_competitor = CompetitorDAO().get(self.event, competitor.get_bib_number())
                valid_run = group.get_valid_run(fetched_competitor)
                #TODO : compute global penalty for this round
                if valid_run is not None:
                    request_url = 'https://www.f3xvault.com/api.php?login=' + login + \
                                  '&password=' + password + \
                                  '&function=postScore&event_id=' + str(self.event.f3x_vault_id) + \
                                  '&pilot_id=' + str(fetched_competitor.get_pilot().f3x_vault_id) + \
                                  '&round=' + str(self.valid_round_number) + \
                                  '&seconds=' + str(valid_run.get_flight_time()) + \
                                  '&penalty=' + str(valid_run.penalty)
                    request_url += '&sub1=' + str(valid_run.chrono.climbout_time)
                    for i in range(0, 10):
                        request_url += '&sub' + str(i + 2) + '=' + str(valid_run.chrono.get_lap_time(i))
                else:
                    #Competitor did not finish its run (or even did not start it !)
                    request_url = 'https://www.f3xvault.com/api.php?login=' + login + \
                                  '&password=' + password + \
                                  '&function=postScore&event_id=' + str(self.event.f3x_vault_id) + \
                                  '&pilot_id=' + str(fetched_competitor.get_pilot().f3x_vault_id) + \
                                  '&round=' + str(self.valid_round_number) + \
                                  '&seconds=' + str(0.0) + \
                                  '&penalty=' + str(0.0)
                    request_url += '&sub1=' + str(0.0)
                    for i in range(0, 10):
                        request_url += '&sub' + str(i + 2) + '=' + str(0.0)
                    request_url += '&dnf=' + str(True)
                response = requests.post(request_url)

        #Update event score status
        valid_integer_code = 0
        if self.valid:
            valid_integer_code = 1
        request_url = 'https://www.f3xvault.com/api.php?login=' + login + \
                      '&password=' + password + \
                      '&function=updateEventRoundStatus&event_id=' + str(self.event.f3x_vault_id) + \
                      '&round_number=' + str(self.valid_round_number) + \
                      '&event_round_score_status=' + str(valid_integer_code)
        response = requests.post(request_url)







