import pandas as pd
from io import StringIO
import requests
from datetime import datetime
import os
import scipy.stats as ss

from F3FChrono.data.Pilot import Pilot
from F3FChrono.data.Competitor import Competitor
from F3FChrono.data.Round import Round
from F3FChrono.data.Chrono import Chrono


class Event:

    def __init__(self):
        self.id = None
        self.begin_date = None
        self.end_date = None
        self.location = ""
        self.name = ""
        self.competitors = {}
        self.rounds = []
        self.min_allowed_wind_speed = 3.0
        self.max_allowed_wind_speed = 25.0
        self.max_wind_dir_dev = 45.0
        self.max_interruption_time = 30 * 60
        self.current_round = None
        self.flights_before_refly = 5
        self.f3x_vault_id = None
        self.number_of_valid_rounds = 0
        self.first_joker_round_number = 4
        self.second_joker_round_number = 15

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

            for index, row in df.iterrows():

                competitor = event.competitor_from_f3x_vault_id(row['Pilot_id'])
                pilot_flight_time = row['seconds']
                pilot_penalty = row['penalty']
                pilot_flight_valid = (pilot_flight_time > 0.0)

                if competitor is not None:
                    pilot_chrono = Chrono()
                    pilot_chrono.run_time = pilot_flight_time
                    f3f_round.handle_terminated_flight(competitor, pilot_chrono, pilot_penalty, pilot_flight_valid)

            print(f3f_round.to_string())

        return event

    def competitor_from_f3x_vault_id(self, f3x_vault_id):
        for key, competitor in self.competitors.items():
            if competitor.get_pilot().get_f3x_vault_id() == f3x_vault_id:
                return competitor
        return None

    def create_new_round(self, insert_database=False):
        f3f_round = Round.new_round(self)
        self.add_existing_round(f3f_round)
        if (insert_database):
            Round.round_dao.insert(f3f_round)

        return f3f_round

    def add_existing_round(self, f3f_round):
        self.rounds.append(f3f_round)
        if self.current_round is None:
            self.current_round = 0
        else:
            self.current_round += 1

    def register_pilot(self, pilot, bib_number, team=None):
        self.competitors[bib_number] = Competitor.register_pilot(self, bib_number, pilot, team)

    def get_current_round(self):
        if len(self.rounds) < 1:
            self.create_new_round(insert_database=True)
        return self.rounds[self.current_round]

    def get_competitor(self, bib_number):
        return self.competitors[bib_number]

    def get_competitors(self):
        return self.competitors

    def set_competitors(self, competitors):
        self.competitors = competitors

    def get_flights_before_refly(self):
        return self.flights_before_refly

    def compute_ranking(self):
        for f3f_round in self.rounds:
            if f3f_round.valid:
                self.number_of_valid_rounds += 1
                for group in f3f_round.groups:
                    group.compute_scores()
                    for bib_number, competitor in self.competitors.items():
                        valid_run = group.get_valid_run(competitor)
                        if valid_run is not None:
                            competitor.score += valid_run.score
                            competitor.update_jokers(f3f_round.round_number, valid_run.score)
                        else:
                            competitor.update_jokers(f3f_round.round_number, 0)

                        #Get penalties
                        runs = group.runs[competitor]
                        for run in runs:
                            competitor.penalty += run.penalty

                    bibs = sorted(self.competitors)
                    pilots_ranks = ss.rankdata([-self.competitors[bib].score_with_jokers(self.number_of_valid_rounds)
                                                for bib in bibs])
                    for i in range(0, len(bibs)):
                        self.competitors[bibs[i]].rank = pilots_ranks[i]
                        self.competitors[bibs[i]].evolutive_rank.append(pilots_ranks[i])


    def to_string(self):
        result=os.linesep+"Event : "+self.name+os.linesep
        for round in self.rounds:
            if (round!=None):
                result+=round.to_string()
        return(result)
