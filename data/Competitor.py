

class Competitor:

    def __init__(self):
        self._bib_number = None
        self._event = None
        self._pilot = None
        self._team = None

    @staticmethod
    def register_pilot(event, bib_number, pilot, team=None):
        competitor = Competitor()
        competitor._event = event
        competitor._pilot = pilot
        competitor._bib_number = bib_number
        competitor._team = team
        return competitor

    def get_pilot(self):
        return self._pilot

    def get_bib_number(self):
        return self._bib_number

    def to_string(self):
        return str(self._bib_number) + '\t' + self._pilot.to_string()

    def __hash__(self):
        return hash(self._bib_number)

    def __lt__(self, other):
        return self._bib_number < other.get_bib_number()
