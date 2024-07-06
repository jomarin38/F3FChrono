#
# This file is part of the F3FChrono distribution (https://github.com/jomarin38/F3FChrono).
# Copyright (c) 2021 Sylvain DAVIET, Joel MARIN.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
from collections import OrderedDict

from F3FChrono.data.dao.RoundDAO import RoundDAO
from F3FChrono.data.dao.RunDAO import RunDAO
import sys

class RoundGroup:

    def __init__(self, f3f_round, group_number):
        self.round = f3f_round
        self.valid = False
        self.start_time = None
        self.end_time = None
        self.group_number = group_number
        self._current_competitor_index = 0
        self._flight_order = []
        self.runs = {}
        self.cancelled = False
        self.group_id = None
        self.rundao=RunDAO()

    def set_flight_order_index(self, index):
        self._current_competitor_index = index

    def set_flight_order(self, flight_order):
        self._flight_order = flight_order
        self._current_competitor_index = 0

    def set_flight_order_from_db(self, serialized_flight_order):
        splitted_line = serialized_flight_order.split(',')
        self._flight_order.clear()
        for str_bib_number in splitted_line:
            self._flight_order.append(int(str_bib_number))

    def get_serialized_flight_order(self):
        res = ''
        for bib_number in self._flight_order:
            res += str(bib_number) + ','
        return res.rstrip(',')

    def get_flight_order(self):
        return self._flight_order

    def get_remaining_bibs_to_fly(self):
        if not self.valid and self._current_competitor_index < len(self._flight_order):
            current_competitor = self.round.event.get_competitor(self._flight_order[self._current_competitor_index])
            if self.get_valid_run(current_competitor) is not None:
                currently_flying_bib = self._current_competitor_index+1
            else:
                currently_flying_bib = self._current_competitor_index
            return self._flight_order[currently_flying_bib:]
        else:
            return []

    #Used in F3XVault export
    def get_valid_flight_order(self, competitor):
        if competitor.bib_number in self._flight_order:
            #remove duplicates, keep last flight for each competitor
            cleaned_flight_order = list(reversed(OrderedDict.fromkeys(reversed(self._flight_order))))
            index = cleaned_flight_order.index(competitor.bib_number)
            return index + 1
        return None

    def next_pilot(self, insert_database=False, visited_competitors=[]):
        if self._current_competitor_index < len(self._flight_order) - 1:
            self._current_competitor_index += 1
            current_competitor = self.get_current_competitor()

            if current_competitor.present:
                return current_competitor
            else:
                if current_competitor not in visited_competitors:
                    # Give him a 0
                    self.round.set_null_flight(current_competitor)
                    visited_competitors.append(current_competitor)
                    return self.next_pilot(insert_database, visited_competitors)
                else:
                    # In this case, nobody is set to present ...
                    return current_competitor
        else:
            return None

    def number_of_performed_runs(self):
        result = 0
        for bib_number, runs_list in self.runs.items():
            result += len(runs_list)
        return result

    def next_pilot_database(self):
        nb_run = self.number_of_performed_runs()
        # if self._current_competitor_index < len(self._flight_order) - 1:
        if nb_run < len(self._flight_order):
            self._current_competitor_index = nb_run
            return self.get_current_competitor()
        else:
            return None

    def validate_group(self, insert_database=False):
        self.valid = True

    def remove_from_flight_order(self, competitor):
        self._flight_order = list(filter(lambda bib: bib != competitor.bib_number, self._flight_order))

    def force_current_competitor(self, competitor):
        if self._flight_order[self._current_competitor_index]!=competitor.get_bib_number():
            self._flight_order.insert(self._current_competitor_index, competitor.get_bib_number())
            #remove the competitor of the flight order
            self._flight_order = (self._flight_order[0:self._current_competitor_index+1] +
                                  [x for x in self._flight_order[self._current_competitor_index+1:]
                                   if x!=competitor.get_bib_number()])

    def has_competitor(self, competitor):
        return (competitor.bib_number in self._flight_order) or (self.get_valid_run(competitor) is not None)

    def get_current_competitor(self):
        return self.round.event.get_competitor(self._flight_order[self._current_competitor_index])

    def set_current_competitor(self, competitor):
        self._current_competitor_index = self._current_competitor_index + \
                                        self._flight_order[self._current_competitor_index:].index(competitor.bib_number)

    def give_refly(self, competitor):
        self._flight_order.insert(self._current_competitor_index + self.round.event.get_flights_before_refly() + 1,
                                  competitor.get_bib_number())
        RoundDAO().update(self.round)

    def add_run(self, run, insert_database=False):
        if run.competitor in self.runs:
            self.runs[run.competitor].append(run)
        else:
            self.runs[run.competitor] = [run]
        if insert_database:
            run_id, chrono_id = self.rundao.insert(run)
            run.id = run_id
            if run.chrono is not None:
                run.chrono.id = chrono_id

    def get_valid_run(self, competitor):
        if competitor in self.runs:
            for run in self.runs[competitor]:
                if run.valid:
                    return run
        return None

    def has_run(self):
        return len(self.runs)>0

    def has_run_competitor(self, competitor):
        if competitor in self.runs:
            return len(self.runs[competitor]) > 0
        else:
            return False

    def cancel_runs_competitor(self, competitor):
        if competitor in self.runs:
            for run in self.runs[competitor]:
                run.valid = False

    def get_penalty(self, competitor):
        penalty = 0
        if competitor in self.runs:
            for run in self.runs[competitor]:
                penalty += run.penalty
        return penalty

    def to_string(self):
        result = ''
        for competitor in sorted(self.runs):
            result += competitor.to_string() + '\t' + self.run_value_as_string(competitor) + os.linesep + os.linesep
        return result

    def run_value_as_string(self, competitor):
        valid_run = self.get_valid_run(competitor)
        if valid_run is not None and valid_run.chrono.run_time is not None:
            return '{:6.2f}'.format(valid_run.chrono.run_time)
        else:
            return 'Flight not valid'

    def run_score_as_string(self, competitor):
        valid_run = self.get_valid_run(competitor)
        if valid_run is not None:
            return str(valid_run.score_as_string())
        else:
            return str(0.0)

    def compute_scores(self):
        if self.has_run():
            run_times = [self.get_valid_run(competitor).get_flight_time() for competitor in sorted(self.runs)
                                 if self.get_valid_run(competitor) and self.get_valid_run(competitor).get_flight_time()]
            if len(run_times) > 0:
                best_run_time = min(run_times)
            else:
                best_run_time = 0
            for competitor in sorted(self.runs):
                valid_run = self.get_valid_run(competitor)
                if valid_run is not None:
                    if not valid_run.get_flight_time():
                        valid_run.score = 0.0
                    else:
                        valid_run.score = best_run_time / valid_run.get_flight_time() * 1000.0

    def get_best_run(self):
        best_run = None
        for competitor, runs in self.runs.items():
            for run in runs:
                if run.valid and (best_run is None or
                                  best_run.get_flight_time() is None or
                                  run.get_flight_time() < best_run.get_flight_time()):
                    best_run = run
        return best_run
