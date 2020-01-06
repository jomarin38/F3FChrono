

class Line:

    def __init__(self, name=None):
        self.name = name
        self.values = []
        self.tag = 'td'

    def set_name(self, name):
        self.name = name

    def add_cell(self, cell):
        self.values.append(cell)

    def start_tag(self):
        return '<'+self.tag+'>'

    def end_tag(self):
        return '</'+self.tag+'>'

    def to_html(self):
        res = '<tr>'
        res += self.start_tag() + self.name.to_html() + self.end_tag()
        for cell in self.values:
            res += self.start_tag() + cell.to_html() + self.end_tag()
        res += '</tr>'
        return res
