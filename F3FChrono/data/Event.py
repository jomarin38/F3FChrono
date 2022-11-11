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

import pandas as pd
from io import StringIO
import requests
from datetime import datetime
import os
import scipy.stats as ss
import random

from F3FChrono.data.Pilot import Pilot
from F3FChrono.data.Competitor import Competitor
from F3FChrono.data.Round import Round
from F3FChrono.data.Chrono import Chrono
from F3FChrono.data.dao.CompetitorDAO import CompetitorDAO
from F3FChrono.data.dao.RoundDAO import RoundDAO


class Event:

    def __init__(self):
        self.id = None
        self.begin_date = None
        self.end_date = None
        self.location = ""
        self.name = ""
        self.competitors = {}
        self.rounds = []
        self.valid_rounds = []
        self.min_allowed_wind_speed = 3
        self.max_allowed_wind_speed = 25
        self.max_wind_dir_dev = 45
        self.max_interruption_time = 30 * 60
        self.current_round = None
        self.bib_start = 1
        self.dayduration = 1
        self.flights_before_refly = 5
        self.f3x_vault_id = None
        self.number_of_valid_rounds = 0
        self.first_joker_round_number = 4
        self.second_joker_round_number = 15
        self.groups_number = 1

    def export_bibs_as_csv(self, csv_writer):
        csv_writer.writerow(['id', 'pilot_name', 'bib_number'])

        for competitor in self.competitors.values():
            row = [str(competitor.get_pilot().get_id()),
                   competitor.get_pilot().to_string(),
                   competitor.get_bib_number()]
            csv_writer.writerow(row)

    def import_bibs(self, csv_file):
        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")

        for line in lines[1:]:
            splitted_line = line.split(',')
            if len(splitted_line)>=3:
                pilot_id = int(splitted_line[0].strip('\"'))
                pilot_bib = int(splitted_line[2].strip('\"'))
                competitor = self.competitor_from_id(pilot_id)
                if competitor is not None:
                    competitor.set_bib_number(pilot_bib)

    @staticmethod
    def from_csv(event_name, event_location, begin_date, end_date, csv_file):
        event = Event()

        event.name = event_name
        event.location = event_location

        event.begin_date = datetime.strptime(begin_date.strip('\"'), '%d/%m/%y')
        event.end_date = datetime.strptime(end_date.strip('\"'), '%d/%m/%y')

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        next_bib_number = 1
        for line in lines:
            splitted_line = line.split(',')
            if len(splitted_line)>=2:
                pilot = Pilot(name=splitted_line[0].strip('\"'),
                              first_name=splitted_line[1].strip('\"')
                              )
                event.register_pilot(pilot, next_bib_number)
                next_bib_number += 1

        return event

    def export_bibs_to_f3xvault(self, f3x_username, f3x_password):
        """
        TODO: f3x_vault related stuff should be moved in specific class later
        :param f3x_username:
        :param f3x_password:
        :return:
        """

        for competitor in self.competitors.values():
            request_url = 'https://www.f3xvault.com/api.php?login=' + f3x_username + \
                          '&password=' + f3x_password + \
                          '&function=updateEventPilot&event_id=' + str(self.f3x_vault_id) + \
                          '&pilot_id=' + str(competitor.get_pilot().get_f3x_vault_id())  + \
                          '&event_pilot_bib=' + str(competitor.get_bib_number())
            requests.post(request_url)

    @staticmethod
    def from_f3x_vault(login, password, contest_id, max_rounds=None):
        """
        TODO: f3x_vault related stuff should be moved in specific class later
        :param login:
        :param password:
        :param contest_id:
        :return:
        """
        event = Event()

        #Getting general event info
        request_url = 'https://www.f3xvault.com/api.php?login=' + login + \
                      '&password=' + password + \
                      '&function=getEventInfo&event_id=' + str(contest_id)
        response = requests.post(request_url)
        splitted_response = response.text.split('\n')

        #Skip first line
        splitted_response.pop(0)

        splitted_line = splitted_response.pop(0).split(',')

        event.id = splitted_line[0].strip('\"')
        #dates have to be converted to datetime objects
        event.name = splitted_line[1].strip('\"')
        event.begin_date = datetime.strptime(splitted_line[3].strip('\"'), '%m/%d/%y')
        event.end_date = datetime.strptime(splitted_line[4].strip('\"'), '%m/%d/%y')
        event.location = splitted_line[2].strip('\"')
        event.f3x_vault_id = contest_id

        n_rounds = int(splitted_line[6].strip('\"'))

        #Skip pilots definition header
        splitted_response.pop(0)

        for line in splitted_response:
            splitted_line = line.split(',')
            if len(splitted_line) > 2:
                pilot = Pilot(name=splitted_line[3].strip('\"'),
                              first_name=splitted_line[2].strip('\"'),
                              f3x_vault_id=int(splitted_line[0].strip('\"')),
                              national_id=splitted_line[7].strip('\"'),
                              fai_id=splitted_line[6].strip('\"')
                              )
                bib_number = int(splitted_line[1].strip('\"'))

                event.register_pilot(pilot, bib_number)

        if max_rounds is not None:
            n_rounds_to_get = min(max_rounds, n_rounds)
        else:
            n_rounds_to_get = n_rounds

        for round_id in range(1, n_rounds_to_get+1):

            f3f_round = event.create_new_round()

            request_url = 'https://www.f3xvault.com/api.php?login=' + login + \
                          '&password=' + password + \
                          '&function=getEventRound&event_id=' + str(contest_id) + \
                          '&round_number=' + str(round_id)
            response = requests.post(request_url)
            df = pd.read_csv(StringIO(response.text), sep=",", header=1)

            f3x_vault_data = {}
            for index, row in df.iterrows():
                #First put data in a dictionary to sort it on bib numbers

                competitor = event.competitor_from_f3x_vault_id(row['Pilot_id'])
                pilot_flight_time = row['seconds']
                pilot_penalty = row['penalty']
                pilot_flight_valid = (pilot_flight_time > 0.0)

                if competitor is not None:
                    pilot_chrono = Chrono()
                    pilot_chrono.run_time = pilot_flight_time
                    f3x_vault_data[competitor.bib_number] = {'competitor' : competitor,
                                                             'pilot_chrono' : pilot_chrono,
                                                             'pilot_penalty' : pilot_penalty,
                                                             'pilot_flight_valid' : pilot_flight_valid}

            for bib in sorted(f3x_vault_data):
                f3f_round.handle_terminated_flight(f3x_vault_data[bib]['competitor'],
                                                   f3x_vault_data[bib]['pilot_chrono'],
                                                   f3x_vault_data[bib]['pilot_penalty'],
                                                   f3x_vault_data[bib]['pilot_flight_valid'])

            f3f_round.validate_round()

            print(f3f_round.to_string())

        return event

    def next_available_bib_number(self):
        return max(self.competitors.keys())+1

    def get_last_round_number(self):
        round_numbers = [f3f_round.round_number for f3f_round in self.rounds]
        if len(round_numbers) > 0:
            return max([f3f_round.round_number for f3f_round in self.rounds])
        else:
            return 0

    def competitor_from_f3x_vault_id(self, f3x_vault_id):
        for key, competitor in self.competitors.items():
            if competitor.get_pilot().get_f3x_vault_id() == f3x_vault_id:
                return competitor
        return None

    def competitor_from_id(self, id):
        for key, competitor in self.competitors.items():
            if competitor.get_pilot().get_id() == id:
                return competitor
        return None

    def create_new_round(self, insert_database=False):
        f3f_round = Round.new_round(self)
        f3f_round.set_flight_order_from_scratch()
        if insert_database:
            Round.round_dao.insert(f3f_round)

        #Get round from database to get group ids
        fully_fetched_round = Round.round_dao.get(f3f_round)
        self.add_existing_round(fully_fetched_round)
        return fully_fetched_round

    def add_existing_round(self, f3f_round):
        self.rounds.append(f3f_round)
        if self.current_round is None:
            self.current_round = 0
        else:
            self.current_round += 1

    def register_pilot(self, pilot, bib_number, team=None):
        new_competitor = Competitor.register_pilot(self, bib_number, pilot, team)
        self.competitors[bib_number] = new_competitor
        return new_competitor

    def unregister_competitor(self, competitor, insert_database=True):
        #This should be possible only if there was no valid flight for this competitor
        if not self.has_run_competitor(competitor):
            self.competitors.pop(competitor.bib_number)
            if insert_database:
                CompetitorDAO().delete(competitor)
        else:
            raise Exception('Too late to delete competitor ' + competitor.display_name() + ' because he flew already !')

    def has_run_competitor(self, competitor):
        res = False
        for f3f_round in self.rounds:
            res = res or f3f_round.has_run_competitor(competitor)

        return res

    def get_current_round(self):
        if len(self.rounds) < 1:
            self.create_new_round(insert_database=True)
        return self.rounds[self.current_round]

    def get_competitor(self, bib_number):
        return self.competitors[bib_number]

    def get_competitors(self):
        return self.competitors

    def get_nb_competitors(self):
        return len(self.competitors)

    def set_competitors(self, competitors):
        self.competitors = competitors

    def get_flights_before_refly(self):
        return self.flights_before_refly

    def random_bib(self):
        self.bib_start = random.randrange(1, self.get_nb_competitors(), 1)
        #Update flying order of current round if no runs were registered
        f3f_round = self.get_current_round()
        if f3f_round is not None and not f3f_round.has_run():
            f3f_round.set_flight_order_from_scratch()
            RoundDAO().update(f3f_round)

    def bib_day_1_compute(self):
        self.bib_start += int(self.get_nb_competitors()/self.dayduration)
        if self.bib_start>self.get_nb_competitors():
            self.bib_start=self.bib_start-self.get_nb_competitors()
        round=self.get_current_round()
        if not round.valid:
            round.cancel_round()

    def compute_ranking(self):
        for f3f_round in self.rounds:
            if f3f_round.valid:
                self.number_of_valid_rounds += 1
                for group in f3f_round.groups:
                    group.compute_scores()
                    for bib_number, competitor in self.competitors.items():
                        if group.has_competitor(competitor):
                            valid_run = group.get_valid_run(competitor)
                            if valid_run is not None:
                                competitor.score += valid_run.score
                                competitor.update_jokers(f3f_round.valid_round_number, valid_run.score)
                            else:
                                competitor.update_jokers(f3f_round.valid_round_number, 0)

                        #Get penalties
                        competitor.penalty += group.get_penalty(competitor)

                bibs = sorted(self.competitors)
                pilots_ranks = ss.rankdata([-self.competitors[bib].score_with_jokers(self.number_of_valid_rounds)
                                            for bib in bibs])
                for i in range(0, len(bibs)):
                    self.competitors[bibs[i]].rank = pilots_ranks[i]
                    self.competitors[bibs[i]].evolutive_rank.append(pilots_ranks[i])
            else:
                #penalties applies also for cancelled rounds
                for group in f3f_round.groups:
                    for bib_number, competitor in self.competitors.items():
                        # Get penalties
                        competitor.penalty += group.get_penalty(competitor)

    def to_string(self):
        result = os.linesep+"Event : "+self.name+os.linesep
        for f3f_round in self.rounds:
            if f3f_round is not None:
                result += f3f_round.to_string()
        return result

    def export_to_f3x_vault(self, login, password, start_round, end_round):
        for i in range(start_round-1, end_round):
            self.rounds[i].rounds.export_to_f3x_vault(login, password)
