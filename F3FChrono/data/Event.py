import pandas as pd
from io import StringIO
import requests

from F3FChrono.data.Pilot import Pilot
from F3FChrono.data.Competitor import Competitor
from F3FChrono.data.Round import Round


class Event:

    def __init__(self):
        self._id = None
        self._begin_date = None
        self._end_date = None
        self._location = ""
        self._name = ""
        self._competitors = {}
        self._rounds = []
        self._min_allowed_wind_speed = 3.0
        self._max_allowed_wind_speed = 25.0
        self._max_wind_dir_dev = 45.0
        self._max_interruption_time = 30 * 60
        self._current_round = None

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

        event._id = splitted_line[0].strip('\"')
        event._begin_date = splitted_line[3].strip('\"')
        event._end_date = splitted_line[4].strip('\"')
        event._location = splitted_line[2].strip('\"')

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
                    f3f_round.handle_terminated_flight(competitor, pilot_flight_time, pilot_penalty, pilot_flight_valid)

            print(f3f_round.to_string())

        return event

    def competitor_from_f3x_vault_id(self, f3x_vault_id):
        for key, competitor in self._competitors.items():
            if competitor.get_pilot().get_f3x_vault_id() == f3x_vault_id:
                return competitor
        return None

    def create_new_round(self):
        f3f_round = Round.new_round(self)
        self._rounds.append(f3f_round)
        if self._current_round is None:
            self._current_round = 0
        else:
            self._current_round += 1
        return f3f_round

    def register_pilot(self, pilot, bib_number):
        self._competitors[bib_number] = Competitor.register_pilot(self, bib_number, pilot)

    def get_current_round(self):
        return self._rounds[self._current_round]

    def get_competitor(self, bib_number):
        return self._competitors[bib_number]
