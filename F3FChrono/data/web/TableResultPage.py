

class TableResultPage:

    def __init__(self, title=None):
        self.title = title
        self.header = None
        self.lines = []

    def set_title(self, title):
        self.title = title

    def set_header(self, header):
        self.header = header

    def add_line(self, line):
        self.lines.append(line)

    def to_html(self):
        res = '<h1>' + self.title + '</h1>'
        res += '<table>'
        res += '<thead>' + self.header.to_html() + '</thead>'
        res += '<tbody>'
        for line in self.lines:
            res += line.to_html()
        res += '</tbody>'
        res += '</table>'
        return res
