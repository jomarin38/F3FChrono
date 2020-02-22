

class Cell:

    def __init__(self, value, joker=False, winner=False, css_id=None):
        self.value = value
        self.joker = joker
        self.winner = winner
        self.css_id = css_id
        if winner:
            self.css_id = 'win'
        if joker:
            self.css_id = 'joker'

    def to_html(self):
        res = self.value
        if self.joker:
            res = '<strike>' + res + '</strike>'
        if self.winner:
            res = '<strong>' + res + '</strong>'
        return res
