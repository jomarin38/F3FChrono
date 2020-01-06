

class ResultPage:

    def __init__(self, title=None):
        self.title = title
        self.tables = []

    def set_title(self, title):
        self.title = title

    def add_table(self, table):
        self.tables.append(table)

    def to_html(self):
        res = '<h1>' + self.title + '</h1>'
        for table in self.tables:
            res += table.to_html()
        return res
