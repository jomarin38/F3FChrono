import os

class ResultPage:

    css_string = None

    def __init__(self, title=None):
        self.title = title
        self.tables = []

    def set_title(self, title):
        self.title = title

    def add_table(self, table):
        self.tables.append(table)

    def to_html(self):
        res = "<html><head><meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">" + \
              "<style>" + ResultPage.get_css_string() + "</style></head><body>"
        res += '<h1>' + self.title + '</h1>'
        for table in self.tables:
            res += table.to_html()


        res+="</body></html>"
        return res

    @staticmethod
    def get_css_string():
        if ResultPage.css_string is None:
            ResultPage.css_string = ''
            css_path = os.path.realpath('F3FChrono/web/f3franking/static/event_view.css')
            with open(css_path) as fp:
                lines = fp.readlines()
                for line in lines:
                    ResultPage.css_string += line

        return ResultPage.css_string
