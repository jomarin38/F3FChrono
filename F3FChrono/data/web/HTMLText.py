

class HTMLText:

    def __init__(self, text=None, css_id=None):
        self.text = text
        self.header = None
        self.lines = []
        self.css_id = css_id

    def set_title(self, title):
        self.text = title

    def set_header(self, header):
        self.header = header

    def add_line(self, line):
        self.lines.append(line)

    def to_html(self):
        res = '<p '
        if self.css_id is not None:
            res += 'id=\"' + self.css_id + '\"'
        res += '>' + self.text + '</p>'
        return res
