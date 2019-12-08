

class Competitor:

    def __init__(self):
        self.bib_number = None
        self.event = None
        self.pilot = None
        self.team = None

    @staticmethod
    def register_pilot(event, bib_number, pilot, team=None):
        competitor = Competitor()
        competitor.event = event
        competitor.pilot = pilot
        competitor.bib_number = bib_number
        competitor.team = team
        return competitor

    def get_pilot(self):
        return self.pilot

    def get_bib_number(self):
        return self.bib_number

    def to_string(self):
        return str(self.bib_number) + '\t' + self.pilot.to_string()

    def display_name(self):
        return self.pilot.to_string()

    def __hash__(self):
        return hash(self.bib_number)

    def __lt__(self, other):
        return self.bib_number < other.get_bib_number()
