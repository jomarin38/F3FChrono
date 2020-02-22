

class ResultTable:

    def __init__(self, title=None, css_id=None):
        self.title = title
        self.header = None
        self.lines = []
        self.css_id = css_id

    def set_title(self, title):
        self.title = title

    def set_header(self, header):
        self.header = header

    def add_line(self, line):
        self.lines.append(line)

    def to_html(self):
        res = '<h2>' + self.title + '</h2>'
        if self.css_id is None:
            res += '<table>'
        else:
            res += '<table id=\"' + self.css_id + '\">'
        res += '<thead>' + self.header.to_html() + '</thead>'
        res += '<tbody>'
        for line in self.lines:
            res += line.to_html()
        res += '</tbody>'
        res += '</table>'
        return res
