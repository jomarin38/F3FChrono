import pandas as pd
from io import StringIO
import requests

from .Pilot import Pilot
from .Competitor import Competitor
from .Round import Round
from .Run import Run

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

    @staticmethod
    def from_f3x_vault(login, password, contest_id):
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
                if len(splitted_line) > 5:
                    fai_id = splitted_line[6].strip('\"')
                else:
                    fai_id = None
                if len(splitted_line) > 6:
                    national_id = splitted_line[7].strip('\"')
                else:
                    national_id = None

                pilot = Pilot(splitted_line[3].strip('\"'), splitted_line[2].strip('\"'),
                              f3x_vault_id=int(splitted_line[0].strip('\"')),
                              national_id=national_id, fai_id=fai_id)
                bib_number = int(splitted_line[1].strip('\"'))
                event._competitors[bib_number] = Competitor.register_pilot(event, bib_number, pilot)

        for round_id in range(1, n_rounds+1):

            f3f_round = Round.new_round(event)
            event._rounds.append(f3f_round)

            request_url = 'https://www.f3xvault.com/api.php?login=' + login + \
                          '&password=' + password + \
                          '&function=getEventRound&event_id=' + str(contest_id) + \
                          '&round_number=' + str(round_id)
            response = requests.post(request_url)
            df = pd.read_csv(StringIO(response.text), sep=",", header=1)

            for index, row in df.iterrows():
                pilot_flight_time = row['seconds']
                pilot_penalty = row['penalty']
                competitor = event.competitor_from_f3x_vault_id(row['Pilot_id'])

                if competitor is not None:
                    run = Run()
                    run.competitor = competitor
                    run.penalty = pilot_penalty
                    run.run_time = pilot_flight_time
                    #Only valid flights are pushed to F3X Vault
                    run.valid = (pilot_flight_time > 0.0)
                    f3f_round.add_run(run)

            print(f3f_round.to_string())

        return event

    def competitor_from_f3x_vault_id(self, f3x_vault_id):
        for key, competitor in self._competitors.items():
            if competitor.get_pilot().get_f3x_vault_id() == f3x_vault_id:
                return competitor
        return None

