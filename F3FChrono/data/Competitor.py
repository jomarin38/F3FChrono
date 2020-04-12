

class Competitor:

    def __init__(self):
        self.bib_number = None
        self.event = None
        self.pilot = None
        self.team = None
        self.rank = None
        self.score = 0.0
        self.evolutive_rank = []
        self.first_joker_round_number = None
        self.first_joker_score = None
        self.second_joker_round_number = None
        self.second_joker_score = None
        self.penalty = 0.0
        self.present = True

    @staticmethod
    def register_pilot(event, bib_number, pilot, team=None, present=True):
        competitor = Competitor()
        competitor.event = event
        competitor.pilot = pilot
        competitor.bib_number = bib_number
        competitor.team = team
        competitor.present = present
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

    def __eq__(self, other):
        return self.bib_number == other.get_bib_number()

    def __ne__(self, other):
        return self.bib_number != other.get_bib_number()

    def compare_rank(self, other):
        return self.rank < other.rank

    def update_jokers(self, round_number, score):
        if self.first_joker_score is None or score < self.first_joker_score:
            self.second_joker_score = self.first_joker_score
            self.second_joker_round_number = self.first_joker_round_number
            self.first_joker_score = score
            self.first_joker_round_number = round_number
        elif self.second_joker_score is None or score < self.second_joker_score:
            self.second_joker_score = score
            self.second_joker_round_number = round_number

    def score_with_jokers(self, number_of_valid_rounds):
        if number_of_valid_rounds < self.event.first_joker_round_number:
            return self.score - self.penalty
        elif number_of_valid_rounds >= self.event.second_joker_round_number:
            return self.score - self.first_joker_score - self.second_joker_score - self.penalty
        else:
            return self.score - self.first_joker_score - self.penalty
