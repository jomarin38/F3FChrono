

class Cell:

    def __init__(self, value, joker=False, winner=False):
        self.value = value
        self.joker = joker
        self.winner = winner

    def to_html(self):
        res = self.value
        if self.joker:
            res = '<strike>' + res + '</strike>'
        if self.winner:
            res = '<strong>' + res + '</strong>'
        return res
