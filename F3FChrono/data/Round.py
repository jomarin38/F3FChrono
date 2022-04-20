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
import copy
import json
import os
from F3FChrono.data.Run import Run
from F3FChrono.data.RoundGroup import RoundGroup
from F3FChrono.data.Chrono import Chrono
from F3FChrono.data.dao.CompetitorDAO import CompetitorDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO
import requests


class Round:

    valid_round_counters = {}
    round_dao = RoundDAO()

    def __init__(self):
        self.event = None
        self.round_number = None
        self.valid_round_number = None
        self.groups = []
        self.valid = False
        self._current_group_index = 0

    @staticmethod
    def new_round(event, add_initial_group=True):
        f3f_round = Round()
        f3f_round.event = event
        f3f_round.round_number = event.get_last_round_number()+1
        if add_initial_group:
            f3f_round.groups.append(RoundGroup(f3f_round, 1))

        return f3f_round

    def set_flight_order_from_scratch(self):
        group_id = self.groups[0].group_id
        self.groups = self.get_groups_from_scratch(1)
        self.groups[0].group_id = group_id

    def get_current_group_index(self):
        return self._current_group_index

    def set_current_group_index(self, group_index):
        self._current_group_index = group_index

    def get_groups_from_scratch(self, number_of_groups):
        groups = [RoundGroup(self, 1)]
        pilots_per_group = int(len(self.event.competitors) / number_of_groups)
        counter = 0
        current_group_index = 0

        flight_order = []
        for bib in [bib_number for bib_number in sorted(self.event.competitors)
                    if bib_number >= self.event.bib_start]:
            if counter < pilots_per_group:
                flight_order += [bib]
                counter += 1
            else:
                groups[current_group_index].set_flight_order(flight_order)
                flight_order = [bib]
                counter = 1
                groups.append(RoundGroup(self, len(groups) + 1))
                current_group_index += 1
        for bib in [bib_number for bib_number in sorted(self.event.competitors)
                    if bib_number < self.event.bib_start]:
            if counter < pilots_per_group:
                flight_order += [bib]
                counter += 1
            else:
                groups[current_group_index].set_flight_order(flight_order)
                flight_order = [bib]
                counter = 1
                groups.append(RoundGroup(self, len(groups) + 1))
                current_group_index += 1
        groups[current_group_index].set_flight_order(flight_order)
        return groups

    def add_group(self, round_group):
        self.groups.append(round_group)

    def group_scoring_enabled(self):
        return len(self.groups) > 1

    def enable_group_scoring(self):
        if len(self.groups) == 1:
            group = self.groups[0]

            new_groups = self.get_groups_from_scratch(self.event.groups_number)
            #Temporary groups to find valid groups
            new_groups2 = self.get_groups_from_scratch(self.event.groups_number)

            #Get runs from base group
            for new_group in new_groups2:
                for bib_number in new_group.get_flight_order():
                    competitor = self.event.get_competitor(bib_number)
                    valid_run = group.get_valid_run(competitor)
                    if valid_run is not None:
                        valid_run = copy.deepcopy(valid_run)
                        if new_group.group_number>1:
                            valid_run.round_group=new_group
                        new_group.add_run(valid_run, insert_database=False)
                        new_group.set_current_competitor(competitor)

            #Cancel flights of competitors that need to refly
            counter = 0
            while counter<len(new_groups2):
                new_group = new_groups2[counter]
                if len(new_group.get_remaining_bibs_to_fly())==0:
                    new_group.validate_group()
                    new_groups[counter] = new_group
                counter += 1

            for bib_number in group.get_flight_order():
                competitor = self.event.get_competitor(bib_number)
                if not new_groups[0].has_competitor(competitor):
                    group.cancel_runs_competitor(competitor)
                    group.remove_from_flight_order(competitor)

            #Check if current group is finished
            first_group_maybe_finished = True
            counter = 0
            while first_group_maybe_finished and counter < len(new_groups[0].get_flight_order()):
                bib_number = new_groups[0].get_flight_order()[counter]
                first_group_maybe_finished = not (bib_number in group.get_remaining_bibs_to_fly())
                counter += 1

            if first_group_maybe_finished:
                group.validate_group()

            self.groups += new_groups[1:]
            #Add new groups in database
            for group in new_groups[1:]:
                Round.round_dao.add_group(group, populate_runs=True)
                group.group_id = Round.round_dao.get_not_cancelled_group_id(self.event.id, self.round_number,
                                                                            group.group_number)

            while (self.groups[self._current_group_index].valid):
                self._current_group_index += 1

            Round.round_dao.update(self)

    def cancel_current_group(self):
        if self.group_scoring_enabled():
            current_group = self.groups[self._current_group_index]
            new_group = RoundGroup(self, current_group.group_number)
            new_group.set_flight_order(current_group.get_flight_order())
            current_group.cancelled = True
            Round.round_dao.update(self)
            Round.round_dao.add_group(new_group)
            new_group.group_id = Round.round_dao.get_not_cancelled_group_id(self.event.id, self.round_number,
                                                                            new_group.group_number)
            self.groups[self._current_group_index] = new_group
            return self.get_current_competitor()
        else:
            return self.cancel_round()

    def get_serialized_flight_order(self):
        res = ''
        for group in self.groups:
            res += group.get_serialized_flight_order() + ','
        return res.rstrip(',')

    def get_flight_order(self):
        res = []
        for group in self.groups:
            res += group.get_flight_order()
        return res

    def get_remaining_bibs_to_fly(self):
        res = []
        for group in self.groups:
            res += group.get_remaining_bibs_to_fly()

        return res


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
        group = self.find_group(competitor)
        group.give_refly(competitor)

    def _add_run(self, run, insert_database=False):
        group = self.find_group(run.competitor)
        run.round_group = group
        group.add_run(run, insert_database)
        group.set_current_competitor(run.competitor)

    def add_run_from_web(self, run):
        group = self.find_group(run.competitor)
        run.round_group = group
        group.add_run(run, True)

    def find_group(self, competitor):
        for group in self.groups:
            if group.has_competitor(competitor):
                return group

    def to_string(self):
        result = os.linesep + 'Round number ' + str(self.round_number) + os.linesep
        for g in self.groups:
            result += g.to_string() + os.linesep
        return result

    def get_current_competitor(self):
        return self.groups[self._current_group_index].get_current_competitor()

    def next_pilot(self, insert_database=False, visited_competitors=[]):

        current_competitor = self.groups[self._current_group_index].next_pilot()

        current_round = self

        if current_competitor is None:
            #Round group is finished, need to switch to next group
            if self._current_group_index < len(self.groups) - 1:
                self.groups[self._current_group_index].validate_group()
                self._current_group_index += 1
                if insert_database:
                    Round.round_dao.update(self)
                current_competitor = self.groups[self._current_group_index].get_current_competitor()
            else:
                #All groups are finished ... need to create a new round
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

    def next_pilot_database(self):
        next_pilot = None

        current_group_index = 0
        while current_group_index < len(self.groups) and next_pilot is None:
            next_pilot = self.groups[current_group_index].next_pilot_database()
            current_group_index += 1

        if next_pilot is not None:
            return next_pilot
        else:
            self.event.create_new_round(insert_database=True)
            return None

    def cancel_round(self):
        self.do_cancel_round()
        self.event.create_new_round(insert_database=True)
        self._current_competitor_index = 0
        return self.get_current_competitor()

    def do_cancel_round(self):
        self.valid = False
        self.valid_round_number = None
        for group in self.groups:
            group.valid = False
        Round.round_dao.update(self)

    def validate_round(self, insert_database=False):
        self.valid = True
        for group in self.groups:
            group.validate_group(insert_database)
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
        visited_competitors = []
        for group in self.groups:
            for bib_number, competitor in self.event.competitors.items():
                fetched_competitor = CompetitorDAO().get(self.event, competitor.get_bib_number())
                valid_run = group.get_valid_run(fetched_competitor)
                #TODO : compute global penalty for this round
                if valid_run is not None:
                    #TODO : handle the case if one competitor has valid flights in several groups
                    order = group.get_valid_flight_order(competitor)
                    request_url = 'https://www.f3xvault.com/api.php?login=' + login + \
                                  '&password=' + password + \
                                  '&function=postScore&event_id=' + str(self.event.f3x_vault_id) + \
                                  '&pilot_id=' + str(fetched_competitor.get_pilot().f3x_vault_id) + \
                                  '&round=' + str(self.valid_round_number) + \
                                  '&seconds=' + str(valid_run.get_flight_time()) + \
                                  '&penalty=' + str(self.get_penalty(competitor)) + \
                                  '&group=' + str(group.group_number)
                    request_url += '&sub1=' + str(valid_run.chrono.climbout_time)
                    for i in range(0, 10):
                        request_url += '&sub' + str(i + 2) + '=' + str(valid_run.chrono.get_lap_time(i))
                    if valid_run is not None:
                        if valid_run.chrono is not None:
                            request_url += '&wind_avg=' + str(valid_run.chrono.mean_wind_speed)
                            request_url += '&dir_avg=' + str(valid_run.chrono.wind_direction)
                        if order is not None:
                            request_url +='&order=' + str(order)
                        response = requests.post(request_url)
                    visited_competitors.append(competitor)
                else:
                    if competitor not in visited_competitors:
                        #Competitor did not finish its run (or even did not start it !)
                        request_url = 'https://www.f3xvault.com/api.php?login=' + login + \
                                      '&password=' + password + \
                                      '&function=postScore&event_id=' + str(self.event.f3x_vault_id) + \
                                      '&pilot_id=' + str(fetched_competitor.get_pilot().f3x_vault_id) + \
                                      '&round=' + str(self.valid_round_number) + \
                                      '&seconds=' + str(0.0) + \
                                      '&penalty=' + str(self.get_penalty(competitor)) + \
                                      '&group=' + str(group.group_number)
                        request_url += '&sub1=' + str(0.0)
                        for i in range(0, 10):
                            request_url += '&sub' + str(i + 2) + '=' + str(0.0)
                        request_url += '&dnf=' + str(True)
                        if valid_run is not None:
                            if valid_run.chrono is not None:
                                request_url += '&wind_avg=' + str(valid_run.chrono.mean_wind_speed)
                                request_url += '&dir_avg=' + str(valid_run.chrono.mean_wind_speed)
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

    def export_to_csv(self, csv_writer):
        csv_writer.writerow(['bib_number', 'pilot_name', 'pilot_firstname', 'round', 'seconds', 'penalty',
                            'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9', 'sub10'])
        for group in self.groups:
            for bib_number in sorted(self.event.competitors):
                competitor = self.event.competitors[bib_number]
                fetched_competitor = CompetitorDAO().get(self.event, competitor.get_bib_number())
                valid_run = group.get_valid_run(fetched_competitor)

                row = [str(fetched_competitor.bib_number), fetched_competitor.get_pilot().name,
                        fetched_competitor.get_pilot().first_name, str(self.valid_round_number)]
                if valid_run is not None:
                    row.append(str(valid_run.get_flight_time()))
                else:
                    row.append('DNF')
                row.append(str(group.get_penalty(competitor)))
                if valid_run is not None:
                    for i in range(0, 10):
                        row.append(str(valid_run.chrono.get_lap_time(i)))
                csv_writer.writerow(row)

    def get_summary_as_json(self, current_round):
        result_dict = {}
        groups = []
        result_dict['weather'] = {}
        if len(self.groups)>0:
            #result_dict['weather']['wind'] = self.groups[-1].runs[list(self.groups[-1].runs.keys())[-1]][0].chrono.mean_wind_speed
            #result_dict['weather']['orient'] = self.groups[-1].runs[list(self.groups[-1].runs.keys())[-1]][0].chrono.wind_direction
            result_dict['weather']['wind'] = self.groups[-1].runs[next(reversed(self.groups[-1].runs))][
                0].chrono.mean_wind_speed
            result_dict['weather']['orient'] = self.groups[-1].runs[next(reversed(self.groups[-1].runs))][
                0].chrono.wind_direction

        result_dict['round'] = str(len(current_round.event.valid_rounds) + 1)
        for group in self.groups:
            if group.get_best_run() is not None:
                group_dict = {'group_number': group.group_number,
                              'best_run': group.get_best_run().to_string()}
            else:
                group_dict = {'group_number': group.group_number}
            groups.append(group_dict)
        result_dict['best_runs'] = groups
        remaining_pilots = []
        for bib_number in self.get_remaining_bibs_to_fly():
            pilot_dict = {'bib_number': bib_number,
                          'pilot_name': self.event.competitors[bib_number].display_name()}
            remaining_pilots.append(pilot_dict)
        result_dict['remaining_pilots'] = remaining_pilots
        return json.dumps(result_dict)
