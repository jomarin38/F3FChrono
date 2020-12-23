from F3FChrono.data.Event import Event


class WinterEvent(Event):

    def __init__(self, successive_pilot_flights):
        super(WinterEvent, self).__init__()
        self._current_rounds = []
        self.successive_pilot_flights = successive_pilot_flights
        self._current_sub_round = 0

    @staticmethod
    def from_csv(event_name, event_location, begin_date, end_date, csv_file):
        event = WinterEvent()
        event._initialize_from_csv(event_name, event_location, begin_date, end_date, csv_file)
        return event

    @staticmethod
    def from_f3x_vault(login, password, contest_id, max_rounds=None):
        event = WinterEvent()
        event._initialize_from_f3x_vault(login, password, contest_id, max_rounds)
        return event

    def create_new_round(self, insert_database=False):
        self._current_rounds.clear()
        for i in range(self.successive_pilot_flights):
            f3f_round = Event.create_new_round(insert_database)
            self._current_rounds.append(f3f_round)
        self._current_sub_round = 0
        return self._current_rounds[self._current_sub_round]


    def get_current_round(self):
        return self._current_rounds[self._current_sub_round]

    def add_existing_round(self, f3f_round):
        super(WinterEvent, self).add_existing_round(f3f_round)
        self._current_rounds.append(f3f_round)
        if len(self._current_rounds)>self.successive_pilot_flights:
            self._current_rounds.pop(0)

    def set_current_round(self, round_number):
        #TODO : implment this method
        pass

    def has_ongoing_round(self):
        return len(self._current_rounds) > 0

    def handle_valid_flight_registered(self):
        self._current_sub_round += 1

    def get_successive_pilot_flights(self):
        return self.successive_pilot_flights